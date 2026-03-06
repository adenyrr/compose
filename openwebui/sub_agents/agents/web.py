"""
Web Agent — navigation, scraping et recherche web.
Modèle : GPT-OSS 120B.
Outil : playwright via MCPO (navigation Chromium headless).
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
You are a web research assistant. You have access to a real Chromium browser via Playwright.
Use the provided browser results to answer questions about web pages, news, current events, or online content.
Summarize findings accurately, quote relevant excerpts, and include source URLs.
Reply in English.
"""


async def run(state: "AlyxState") -> dict:
    messages = state.get("messages", [])
    user_text = _last_user_message(messages)

    # Tenter une navigation/recherche avec playwright
    browser_result = ""
    try:
        # Chercher une URL dans la query
        url = _extract_url(user_text)
        if url:
            nav = await call_tool("playwright", "browser_navigate", {"url": url})
            content = await call_tool("playwright", "browser_get_content", {})
            browser_result = f"Page: {url}\n{json.dumps(content, ensure_ascii=False)[:3000]}"
        else:
            # DuckDuckGo via playwright si pas d'URL directe
            search_url = f"https://duckduckgo.com/?q={user_text.replace(' ', '+')}&ia=web"
            await call_tool("playwright", "browser_navigate", {"url": search_url})
            snapshot = await call_tool("playwright", "browser_snapshot", {})
            browser_result = json.dumps(snapshot, ensure_ascii=False)[:3000]
    except Exception as exc:
        browser_result = f"Browser navigation failed: {exc}"

    llm = ChatOpenAI(
        model=_MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0.2,
    )

    prompt = f"## Browser result\n{browser_result}\n\nUser question: {user_text}"
    response = await llm.ainvoke([
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=prompt),
    ])

    return {"agent_outputs": {"web": response.content}}


def _extract_url(text: str) -> str:
    import re
    match = re.search(r"https?://[^\s]+", text)
    return match.group(0) if match else ""


def _last_user_message(messages: list) -> str:
    for msg in reversed(messages):
        if msg.type == "human":
            return msg.content if isinstance(msg.content, str) else ""
    return ""
