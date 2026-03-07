"""
Graph Builder — assemble le StateGraph LangGraph.

Architecture :
  supervisor → (agents sélectionnés en parallèle) → END

La persistance est assurée par PostgresSaver (DB langgraph).
Le thread_id correspond au chat_id OpenWebUI pour l'historique multi-tours.
"""

from __future__ import annotations

from functools import partial
from typing import Callable

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg_pool import AsyncConnectionPool

from graph.state import AlyxState
from graph.supervisor import route
import agents.vision as vision_agent
import agents.scholar as scholar_agent
import agents.coder as coder_agent
import agents.tech as tech_agent
import agents.web as web_agent
import agents.media as media_agent
import agents.data as data_agent
import agents.memory_agent as memory_mod
import agents.image_gen as image_gen_agent
import agents.rag_agent as rag_agent

_AGENT_MAP: dict[str, Callable] = {
    "vision":    vision_agent.run,
    "scholar":   scholar_agent.run,
    "coder":     coder_agent.run,
    "tech":      tech_agent.run,
    "web":       web_agent.run,
    "media":     media_agent.run,
    "data":      data_agent.run,
    "memory":    memory_mod.run,
    "image_gen": image_gen_agent.run,
    "rag":       rag_agent.run,
}


def _routing_condition(state: AlyxState) -> list[str]:
    """Retourne les nœuds agents à invoquer (fan-out parallèle)."""
    routing = state.get("routing", [])
    return routing if routing else [END]


def _merge_agent_output(state: AlyxState, agent_name: str, output: dict) -> AlyxState:
    """Fusionne la sortie d'un agent dans l'état partagé."""
    current_outputs = dict(state.get("agent_outputs", {}))
    current_outputs.update(output.get("agent_outputs", {}))

    current_artifacts = list(state.get("artifacts", []))
    current_artifacts.extend(output.get("artifacts", []))

    return {**state, "agent_outputs": current_outputs, "artifacts": current_artifacts}


async def build_graph(db_url: str, models: dict | None = None):
    """
    Construit et compile le graphe LangGraph avec persistance PostgreSQL.

    Args:
        db_url: connection string PostgreSQL pour LangGraph (DB langgraph).
        models: dict optionnel de modèles par nom de nœud (supervisor, vision, …).

    Returns:
        Graphe compilé prêt à l'usage.
    """
    _models = models or {}
    builder = StateGraph(AlyxState)

    # Nœud superviseur
    builder.add_node("supervisor", partial(route, model=_models.get("supervisor")))
    builder.set_entry_point("supervisor")

    # Nœuds agents
    for name, fn in _AGENT_MAP.items():
        builder.add_node(name, partial(fn, model=_models.get(name)))

    # Edge conditionnel depuis le superviseur → agents ou END
    builder.add_conditional_edges(
        "supervisor",
        _routing_condition,
        {**{name: name for name in _AGENT_MAP}, END: END},
    )

    # Tous les agents terminent → END
    for name in _AGENT_MAP:
        builder.add_edge(name, END)

    # Checkpointer PostgreSQL via pool de connexions persistant
    pool = AsyncConnectionPool(conninfo=db_url, max_size=20, open=False)
    await pool.open()
    checkpointer = AsyncPostgresSaver(pool)
    await checkpointer.setup()

    graph = builder.compile(checkpointer=checkpointer)
    # Retourner le pool pour maintenir les connexions vivantes
    return graph, pool
