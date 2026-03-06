"""
AlyxState — état partagé du graphe LangGraph.
Tous les nœuds lisent et écrivent sur ce TypedDict.
"""

from __future__ import annotations

from typing import Annotated, Any
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AlyxState(TypedDict):
    # Historique de la conversation (add_messages = append-only reducer)
    messages: Annotated[list[BaseMessage], add_messages]

    # Images base64 extraites du message courant par la pipeline
    images_b64: list[str]

    # Liste des agents sélectionnés par le superviseur pour ce tour
    routing: list[str]

    # Sorties brutes de chaque agent invoqué, indexées par nom d'agent
    agent_outputs: dict[str, str]

    # Artifacts générés (blocs html/js/py, images url…) à passer à Alyx
    artifacts: list[dict[str, Any]]
