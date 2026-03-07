"""
title: Alyx
author: adenyrr
version: 0.3.0
requirements: langgraph>=0.2, langchain-core>=0.3, langchain-openai>=0.2, langgraph-checkpoint-postgres, psycopg[pool], httpx>=0.27, mcp, openai>=1.0, pydantic>=2.0
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

import asyncio
import os
import sys
import threading
from typing import Generator

# Garantit que graph/, agents/, tools/ sont importables depuis /app/pipelines/
_PIPELINES_DIR = os.path.dirname(os.path.abspath(__file__))
if _PIPELINES_DIR not in sys.path:
    sys.path.insert(0, _PIPELINES_DIR)

# Pydantic est nécessaire à la définition de Valves (module level).
# On l'importe avec un fallback pour garantir que le module charge
# même avant que les requirements soient installés.
try:
    from pydantic import BaseModel, Field
except ImportError:  # premier chargement, avant install des deps
    BaseModel = object  # type: ignore[assignment,misc]
    def Field(default=None, **_kwargs):  # type: ignore[misc]
        return default

# Valeurs d'environnement — servent de défauts pour les Valves
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")
_DB_URL = os.environ.get("DATABASE_URL", "")

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
    from langchain_core.messages import HumanMessage, AIMessage  # lazy
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
    class Valves(BaseModel):
        # --- Connexion ---
        litellm_url: str = Field(default=_LITELLM_URL, description="LiteLLM API URL")
        litellm_api_key: str = Field(default=_LITELLM_API_KEY, description="LiteLLM API key")
        db_url: str = Field(default=_DB_URL, description="PostgreSQL connection string (LangGraph checkpoint)")
        # --- Alyx (synthèse finale) ---
        alyx_model: str = Field(default="openrouter/gpt-oss", description="Modèle de synthèse finale d'Alyx")
        alyx_temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Température de synthèse Alyx")
        history_messages: int = Field(default=12, ge=2, le=40, description="Nombre de messages d'historique envoyés à Alyx")
        # --- Comportement ---
        stream_agent_status: bool = Field(default=True, description="Streamer une ligne de statut avant la réponse (agents invoqués)")
        enable_memory_bg: bool = Field(default=True, description="Activer la condensation mémoire en arrière-plan")
        # --- Superviseur ---
        supervisor_model: str = Field(default="openrouter/gpt-oss", description="Modèle du superviseur (routage)")
        # --- Modèles agents ---
        model_vision: str = Field(default="openrouter/qwen3.5-flash", description="Modèle Vision")
        model_scholar: str = Field(default="openrouter/gpt-oss", description="Modèle Scholar")
        model_coder: str = Field(default="openrouter/kimi-k2.5", description="Modèle Coder")
        model_tech: str = Field(default="openrouter/kimi-k2.5", description="Modèle Tech")
        model_web: str = Field(default="openrouter/gpt-oss", description="Modèle Web")
        model_media: str = Field(default="openrouter/gpt-oss", description="Modèle Media")
        model_data: str = Field(default="openrouter/gpt-oss", description="Modèle Data")
        model_memory: str = Field(default="openrouter/gpt-oss", description="Modèle Memory")
        model_image_gen: str = Field(default="pollinations/flux", description="Modèle ImageGen")
        model_rag: str = Field(default="openrouter/gpt-oss", description="Modèle RAG")

    def __init__(self):
        self.name = "Alyx"
        self.valves = self.Valves()
        self._graph = None
        self._pool = None
        # Loop persistant dans un thread dédié — toutes les ops async partagent le même loop
        # pour que les connexions psycopg (liées à leur loop) restent valides.
        self._loop = asyncio.new_event_loop()
        threading.Thread(
            target=self._loop.run_forever,
            daemon=True,
            name="alyx-async",
        ).start()

    def on_valves_updated(self):
        """Invalide le graphe pour forcer un rebuild avec les nouveaux paramètres."""
        old_pool = self._pool
        self._graph = None
        self._pool = None
        if old_pool is not None:
            asyncio.run_coroutine_threadsafe(old_pool.close(), self._loop)

    def _run_sync(self, coro, timeout: int = 300):
        """Exécute une coroutine dans le loop persistant depuis un thread synchrone."""
        return asyncio.run_coroutine_threadsafe(coro, self._loop).result(timeout=timeout)

    def _ensure_graph(self):
        """Initialise le graphe LangGraph une fois (lazy).

        On purge graph.builder (et les agents/tools) du cache sys.modules avant
        chaque (re-)build, pour que les modifications sur disque soient toujours
        prises en compte sans redémarrer le container.
        """
        if self._graph is not None:
            return self._graph

        # Invalider le cache des sous-modules Alyx pour forcer une relecture disque
        _submodule_prefixes = ("graph.", "agents.", "tools.")
        for key in list(sys.modules):
            if any(key == p.rstrip(".") or key.startswith(p) for p in _submodule_prefixes):
                del sys.modules[key]

        from graph.builder import build_graph
        models = {
            "supervisor": self.valves.supervisor_model,
            "vision":     self.valves.model_vision,
            "scholar":    self.valves.model_scholar,
            "coder":      self.valves.model_coder,
            "tech":       self.valves.model_tech,
            "web":        self.valves.model_web,
            "media":      self.valves.model_media,
            "data":       self.valves.model_data,
            "memory":     self.valves.model_memory,
            "image_gen":  self.valves.model_image_gen,
            "rag":        self.valves.model_rag,
        }
        self._graph, self._pool = self._run_sync(build_graph(self.valves.db_url, models))
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
        Toutes les opérations async s'exécutent dans le loop persistant de l'instance
        via run_coroutine_threadsafe, garantissant que les connexions psycopg restent valides.
        """

        # 1. Préparer l'état initial
        from langchain_core.messages import HumanMessage  # lazy
        from openai import OpenAI  # lazy
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

        # 2. Exécuter le graphe (supervisor + agents) dans le loop persistant
        try:
            graph = self._ensure_graph()
        except Exception as exc:
            yield f"[Erreur d'initialisation du graphe : {exc}]"
            return

        agent_outputs: dict[str, str] = {}
        artifacts: list[dict] = []

        try:
            agent_outputs, artifacts = self._run_sync(
                self._run_graph(graph, initial_state, config)
            )
        except Exception as exc:
            yield f"[Erreur lors de l'exécution : {exc}]"
            return

        # 3. Synthèse finale streamée par Alyx (client sync OpenAI)
        synthesis_context = _build_synthesis_context(agent_outputs, artifacts)

        # Ligne de statut agents (optionnelle)
        if self.valves.stream_agent_status and agent_outputs:
            labels = " · ".join(
                _AGENT_ICONS.get(name, name)
                for name in agent_outputs
                if agent_outputs[name] and agent_outputs[name].strip()
            )
            if labels:
                yield f"> *Agents : {labels}*\n\n"

        synth_messages = [{"role": "system", "content": _ALYX_SYSTEM}]
        # Historique récent
        for m in messages[-self.valves.history_messages:]:
            synth_messages.append({"role": m.get("role", "user"), "content": m.get("content", "")})

        if synthesis_context:
            synth_messages.append({
                "role": "user",
                "content": f"[Résultats des agents spécialisés]\n{synthesis_context}\n\n[Message original de l'utilisateur]\n{user_message}",
            })
        else:
            synth_messages.append({"role": "user", "content": user_message})

        client = OpenAI(base_url=self.valves.litellm_url, api_key=self.valves.litellm_api_key)
        stream = client.chat.completions.create(
            model=self.valves.alyx_model,
            messages=synth_messages,
            temperature=self.valves.alyx_temperature,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                yield delta.content

        # 4. Condensation mémoire en arrière-plan (true fire-and-forget)
        if self.valves.enable_memory_bg:
            try:
                import agents.memory_agent as memory_mod
                final_state = {
                    "messages": lc_messages + [HumanMessage(content=user_message)],
                    "images_b64": images_b64,
                    "routing": [],
                    "agent_outputs": agent_outputs,
                    "artifacts": artifacts,
                }
                asyncio.run_coroutine_threadsafe(
                    memory_mod.run_bg(final_state, model=self.valves.model_memory),
                    self._loop,
                )
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
