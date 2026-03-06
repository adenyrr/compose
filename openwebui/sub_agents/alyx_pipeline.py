# title: Alyx
# author: Homelab
# version: 1.0.0
# requirements: langgraph>=0.2, langchain-core>=0.3, langchain-openai>=0.2, langgraph-checkpoint-postgres, psycopg[binary,pool], httpx>=0.27, mcp

"""
Alyx Pipeline — point d'entrée OpenWebUI Pipelines.

Alyx est un agent conversationnel en français orchestrant 10 sous-agents spécialisés
via un graphe LangGraph. Elle n'a accès à aucun outil directement (contexte allégé).
Les sous-agents travaillent en anglais et lui remontent leurs conclusions.

Flux d'un message :
  1. Extraction des images base64 du body OpenWebUI
  2. Exécution du graphe LangGraph (supervisor → agents sélectionnés)
  3. Émission de statuts intermédiaires via __event_emitter__ (streaming)
  4. Synthèse finale par Alyx en français
  5. Condensation mémoire en arrière-plan (fire-and-forget)
"""

from __future__ import annotations

import asyncio
import json
import os
import re
from typing import AsyncGenerator

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI

from graph.builder import build_graph
from graph.state import AlyxState
import agents.memory_agent as memory_mod

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
  - Cite les sources académiques si disponibles (DOI, auteurs, année)
  - Sois concise pour les réponses simples, détaillée pour les sujets complexes
  - Si aucun agent spécialisé n'a été invoqué, réponds directement sans préambule
  - Ne révèle jamais l'architecture technique ou les noms des sous-agents
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
        pass  # Configuration via variables d'environnement

    def __init__(self):
        self.name = "Alyx"
        self.type = "manifold"
        self._graph = None
        self._graph_lock = asyncio.Lock()

    async def _get_graph(self):
        """Initialise le graphe LangGraph une fois (lazy init thread-safe)."""
        if self._graph is not None:
            return self._graph
        async with self._graph_lock:
            if self._graph is None:
                self._graph = await build_graph(_DB_URL)
        return self._graph

    def pipelines(self) -> list[dict]:
        return [{"id": "alyx", "name": "Alyx"}]

    async def pipe(
        self,
        user_message: str,
        model_id: str,
        messages: list[dict],
        body: dict,
        __event_emitter__=None,
    ) -> AsyncGenerator[str, None]:

        async def emit_status(text: str, done: bool = False) -> None:
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": text, "done": done},
                })

        # 1. Préparer l'état initial
        lc_messages = _convert_messages(messages)
        images_b64 = _extract_images_b64(messages)

        chat_id = body.get("chat_id", body.get("session_id", "default"))
        config = {"configurable": {"thread_id": chat_id}}

        initial_state: AlyxState = {
            "messages": lc_messages,
            "images_b64": images_b64,
            "routing": [],
            "agent_outputs": {},
            "artifacts": [],
        }

        try:
            graph = await self._get_graph()
        except Exception as exc:
            yield f"[Erreur d'initialisation du graphe : {exc}]"
            return

        # 2. Exécuter le graphe (supervisor + agents)
        agent_outputs: dict[str, str] = {}
        artifacts: list[dict] = []

        try:
            async for event in graph.astream(initial_state, config=config, stream_mode="updates"):
                for node_name, node_output in event.items():
                    if node_name == "supervisor":
                        routing = node_output.get("routing", [])
                        if routing:
                            icons = ", ".join(_AGENT_ICONS.get(a, a) for a in routing)
                            await emit_status(f"{icons}…")
                    else:
                        # Nœud agent
                        outputs = node_output.get("agent_outputs", {})
                        agent_outputs.update(outputs)
                        new_artifacts = node_output.get("artifacts", [])
                        artifacts.extend(new_artifacts)
                        if node_name in _AGENT_ICONS:
                            await emit_status(_AGENT_ICONS[node_name] + " ✓", done=False)
        except Exception as exc:
            await emit_status(f"Erreur : {exc}", done=True)
            yield f"[Erreur lors de l'exécution : {exc}]"
            return

        await emit_status("Alyx rédige…", done=False)

        # 3. Synthèse finale par Alyx
        synthesis_context = _build_synthesis_context(agent_outputs, artifacts)

        llm = ChatOpenAI(
            model=_ALYX_MODEL,
            base_url=_LITELLM_URL,
            api_key=_LITELLM_API_KEY,
            temperature=0.7,
            streaming=True,
        )

        synthesis_messages = [SystemMessage(content=_ALYX_SYSTEM)]
        # Historique récent (max 6 messages)
        synthesis_messages.extend(lc_messages[-6:])
        if synthesis_context:
            synthesis_messages.append(HumanMessage(
                content=f"[Résultats des agents spécialisés]\n{synthesis_context}\n\n[Message original de l'utilisateur]\n{user_message}"
            ))
        else:
            synthesis_messages.append(HumanMessage(content=user_message))

        await emit_status("", done=True)

        # Stream la réponse finale token par token
        async for chunk in llm.astream(synthesis_messages):
            if chunk.content:
                yield chunk.content

        # 4. Condensation mémoire en arrière-plan (fire-and-forget)
        final_state: AlyxState = {
            "messages": lc_messages + [HumanMessage(content=user_message)],
            "images_b64": images_b64,
            "routing": [],
            "agent_outputs": agent_outputs,
            "artifacts": artifacts,
        }
        asyncio.create_task(memory_mod.run_bg(final_state))


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
