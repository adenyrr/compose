"""
title: Alyx
author: adenyrr
version: 1.2.0
requirements: langgraph>=0.2, langchain-core>=0.3, langchain-openai>=0.2, langgraph-checkpoint-postgres, psycopg[binary,pool], httpx>=0.27, mcp, openai>=1.0
"""

"""
Alyx Pipeline — point d'entrée OpenWebUI Pipelines.

Alyx est un agent conversationnel en français orchestrant 10 sous-agents spécialisés
via un graphe LangGraph. Elle n'a accès à aucun outil directement (contexte allégé).
Les sous-agents travaillent en anglais et lui remontent leurs conclusions.

Flux d'un message :
  1. Extraction des images base64 du body OpenWebUI
  2. Exécution du graphe LangGraph (supervisor → agents sélectionnés)
  3. Synthèse finale streamée par Alyx en français
  4. Condensation mémoire en arrière-plan (fire-and-forget)
"""

from __future__ import annotations

import asyncio
import os
import sys
from typing import Generator

# Garantit que graph/, agents/, tools/ sont importables depuis /app/pipelines/
_PIPELINES_DIR = os.path.dirname(os.path.abspath(__file__))
if _PIPELINES_DIR not in sys.path:
    sys.path.insert(0, _PIPELINES_DIR)

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from openai import OpenAI

_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")
_DB_URL = os.environ.get("DATABASE_URL", "")
_ALYX_MODEL = "openrouter/gpt-oss"

# Icônes de statut par agent
_AGENT_ICONS = {
    "vision":    "📷 Vision",
    "scholar":   "🔬 Scholar",
    "coder":     "💻 Coder",
    "tech":      "🔧 Tech",
    "web":       "🌐 Web",
    "media":     "🎬 Media",
    "data":      "📊 Data",
    "memory":    "🧠 Memory",
    "image_gen": "🎨 ImageGen",
    "rag":       "📚 RAG",
}

_ALYX_SYSTEM = """\
Tu es Alyx, une assistante IA conversationnelle intelligente, chaleureuse et précise.
Tu t'exprimes EXCLUSIVEMENT en français, quelles que soient la langue ou la formulation de l'utilisateur.

Tu orchestres des agents spécialisés qui travaillent en arrière-plan pour toi.
Quand leurs résultats te sont fournis, intègre-les naturellement dans ta réponse sans mentionner
les détails techniques du pipeline (noms d'agents, processus interne, etc.).

Directives :
  - Réponds toujours en français, de façon fluide et naturelle
  - Si un agent a généré un artifact (bloc ```html, ```javascript, ```python), inclus-le tel quel dans ta réponse
  - Si une image a été générée (lien markdown ![...](url)), inclus le lien tel quel
  - Cite toujours tes sources, académiques si disponibles (DOI, auteurs, année)
  - Sois concise pour les réponses simples, détaillée pour les sujets complexes
  - Si aucun agent spécialisé n'a été invoqué, réponds directement sans préambule
"""


def _convert_messages(messages: list[dict]) -> list:
    """Convertit le format OpenWebUI en messages LangChain."""
    lc_messages = []
    for m in messages:
        role = m.get("role", "")
        content = m.get("content", "")
        if isinstance(content, list):
            # Garder uniquement le texte pour l'historique (les images sont dans images_b64)
            content = " ".join(
                part.get("text", "") for part in content if isinstance(part, dict) and part.get("type") == "text"
            )
        if role == "user":
            lc_messages.append(HumanMessage(content=content))
        elif role == "assistant":
            lc_messages.append(AIMessage(content=content))
    return lc_messages


def _extract_images_b64(messages: list[dict]) -> list[str]:
    """Extrait les images base64 du dernier message utilisateur."""
    images: list[str] = []
    for m in reversed(messages):
        if m.get("role") != "user":
            continue
        content = m.get("content", "")
        if isinstance(content, list):
            for part in content:
                if isinstance(part, dict) and part.get("type") == "image_url":
                    url = part.get("image_url", {}).get("url", "")
                    if url.startswith("data:"):
                        # Extraire la partie base64 après la virgule
                        b64 = url.split(",", 1)[-1]
                        images.append(b64)
        break
    return images


class Pipeline:
    class Valves:
        pass

    def __init__(self):
        self.name = "Alyx"
        self._graph = None

    def _ensure_graph(self):
        """Initialise le graphe LangGraph une fois (lazy)."""
        if self._graph is not None:
            return self._graph
        from graph.builder import build_graph
        loop = asyncio.new_event_loop()
        try:
            self._graph = loop.run_until_complete(build_graph(_DB_URL))
        finally:
            loop.close()
        return self._graph

    def pipe(
        self,
        user_message: str,
        model_id: str,
        messages: list[dict],
        body: dict,
    ) -> Generator[str, None, None]:
        """
        Point d'entrée synchrone (Generator) exigé par le framework Pipelines.
        Le graphe LangGraph (async) est exécuté dans un event loop éphémère,
        puis la synthèse est streamée via le client OpenAI sync.
        """

        # 1. Préparer l'état initial
        lc_messages = _convert_messages(messages)
        images_b64 = _extract_images_b64(messages)

        chat_id = body.get("chat_id", body.get("session_id", "default"))
        config = {"configurable": {"thread_id": chat_id}}

        initial_state = {
            "messages": lc_messages,
            "images_b64": images_b64,
            "routing": [],
            "agent_outputs": {},
            "artifacts": [],
        }

        # 2. Exécuter le graphe (supervisor + agents) — async dans un loop dédié
        try:
            graph = self._ensure_graph()
        except Exception as exc:
            yield f"[Erreur d'initialisation du graphe : {exc}]"
            return

        agent_outputs: dict[str, str] = {}
        artifacts: list[dict] = []

        loop = asyncio.new_event_loop()
        try:
            agent_outputs, artifacts = loop.run_until_complete(
                self._run_graph(graph, initial_state, config)
            )
        except Exception as exc:
            yield f"[Erreur lors de l'exécution : {exc}]"
            return
        finally:
            loop.close()

        # 3. Synthèse finale streamée par Alyx (client sync OpenAI)
        synthesis_context = _build_synthesis_context(agent_outputs, artifacts)

        synth_messages = [{"role": "system", "content": _ALYX_SYSTEM}]
        # Historique récent (max 6 échanges)
        for m in messages[-12:]:
            synth_messages.append({"role": m.get("role", "user"), "content": m.get("content", "")})

        if synthesis_context:
            synth_messages.append({
                "role": "user",
                "content": f"[Résultats des agents spécialisés]\n{synthesis_context}\n\n[Message original de l'utilisateur]\n{user_message}",
            })
        else:
            synth_messages.append({"role": "user", "content": user_message})

        client = OpenAI(base_url=_LITELLM_URL, api_key=_LITELLM_API_KEY)
        stream = client.chat.completions.create(
            model=_ALYX_MODEL,
            messages=synth_messages,
            temperature=0.7,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                yield delta.content

        # 4. Condensation mémoire en arrière-plan (fire-and-forget)
        try:
            bg_loop = asyncio.new_event_loop()
            final_state = {
                "messages": lc_messages + [HumanMessage(content=user_message)],
                "images_b64": images_b64,
                "routing": [],
                "agent_outputs": agent_outputs,
                "artifacts": artifacts,
            }
            import agents.memory_agent as memory_mod
            bg_loop.run_until_complete(memory_mod.run_bg(final_state))
            bg_loop.close()
        except Exception:
            pass  # ne jamais bloquer la réponse pour la mémoire

    @staticmethod
    async def _run_graph(graph, initial_state: dict, config: dict):
        """Exécute le graphe LangGraph et collecte les sorties agents."""
        agent_outputs: dict[str, str] = {}
        artifacts: list[dict] = []

        async for event in graph.astream(initial_state, config=config, stream_mode="updates"):
            for node_name, node_output in event.items():
                if node_name == "supervisor":
                    continue
                outputs = node_output.get("agent_outputs", {})
                agent_outputs.update(outputs)
                new_artifacts = node_output.get("artifacts", [])
                artifacts.extend(new_artifacts)

        return agent_outputs, artifacts


def _build_synthesis_context(agent_outputs: dict[str, str], artifacts: list[dict]) -> str:
    """Construit le contexte de synthèse à injecter dans le prompt Alyx."""
    parts: list[str] = []

    for agent_name, output in agent_outputs.items():
        if output and output.strip():
            label = _AGENT_ICONS.get(agent_name, agent_name)
            parts.append(f"## {label}\n{output}")

    for artifact in artifacts:
        if artifact.get("type") == "image" and artifact.get("url"):
            parts.append(f"## Image générée\n![Image]({artifact['url']})")

    return "\n\n".join(parts)
