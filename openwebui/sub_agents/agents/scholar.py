"""
Scholar Agent — recherche académique et scientifique.
Outils : paper-search (MCPO), wikipedia (MCPO), sequential-thinking (MCPO).
Modèle : GPT-OSS 120B.
"""

from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from tools.mcpo_client import call_tool

if TYPE_CHECKING:
    from graph.state import AlyxState

_MODEL = "openrouter/gpt-oss"
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")

_SYSTEM = """\
You are an academic research specialist. Use the provided tool results to answer scientific questions.
Always cite DOIs, authors, and publication years when available.
Prioritize peer-reviewed sources. Reply in English with structured markdown.
"""


async def run(state: "AlyxState") -> dict:
    messages = state.get("messages", [])
    user_text = _last_user_message(messages)

    # 1. Recherche académique
    paper_results = ""
    wiki_results = ""
    reasoning = ""

    try:
        papers = await call_tool("paper-search", "search_papers", {"query": user_text, "limit": 5})
        paper_results = json.dumps(papers, ensure_ascii=False, indent=2)
    except Exception as exc:
        paper_results = f"paper-search unavailable: {exc}"

    try:
        wiki = await call_tool("wikipedia", "search", {"query": user_text, "limit": 3})
        wiki_results = json.dumps(wiki, ensure_ascii=False, indent=2)
    except Exception as exc:
        wiki_results = f"wikipedia unavailable: {exc}"

    try:
        seq = await call_tool("sequential-thinking", "think", {"thought": user_text})
        reasoning = json.dumps(seq, ensure_ascii=False, indent=2)
    except Exception:
        pass

    # 2. Synthèse LLM
    context = (
        f"## Paper search results\n{paper_results}\n\n"
        f"## Wikipedia results\n{wiki_results}\n\n"
        f"## Sequential reasoning\n{reasoning}".strip()
    )

    llm = ChatOpenAI(
        model=_MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0.2,
    )

    response = await llm.ainvoke([
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=f"{context}\n\nUser question: {user_text}"),
    ])

    return {"agent_outputs": {"scholar": response.content}}


def _last_user_message(messages: list) -> str:
    for msg in reversed(messages):
        if msg.type == "human":
            return msg.content if isinstance(msg.content, str) else ""
    return ""
