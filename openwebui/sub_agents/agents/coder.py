"""
Coder Agent — génération de code, artifacts et fichiers téléchargeables.
Modèle : kimi-k2.5.
Outils : git (MCPO), open-terminal pour validation.

Génère des artifacts OpenWebUI natifs via des fences de code :
  ```html   → rendu HTML interactif
  ```javascript → sandbox JS
  ```python  → sandbox Pyodide
Les fichiers téléchargeables sont inclus dans le bloc markdown.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from tools.mcpo_client import call_tool

if TYPE_CHECKING:
    from graph.state import AlyxState

_MODEL = "openrouter/kimi-k2.5"
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")

_SYSTEM = """\
You are an expert software engineer and creative front-end developer.
When asked to create interactive UI, charts, games, or visualizations, output a SINGLE
self-contained artifact using the appropriate code fence:
  - Interactive HTML/CSS/JS  → ```html
  - Pure JavaScript          → ```javascript
  - Python analysis/script   → ```python

Artifact rules:
  - The artifact must be entirely self-contained (no external imports unless CDN-hosted).
  - Use dark theme (#0f1117 background) as default.
  - Do NOT output explanations inside the artifact — only clean code.
  - After the artifact, provide a short explanation in plain English.

For downloadable files (CSV, JSON, config files), wrap them in the correct language fence
and add a comment at the top: `# filename: suggested_name.ext`.

When you need git operations, use the provided git tool results.
Always reply in English.
"""


async def run(state: "AlyxState") -> dict:
    messages = state.get("messages", [])
    user_text = _last_user_message(messages)

    # Tente d'obtenir le contexte git si pertinent
    git_context = ""
    if any(kw in user_text.lower() for kw in ["git", "commit", "diff", "branch", "repo"]):
        try:
            git_info = await call_tool("git", "git_status", {})
            git_context = f"\n## Git status\n{git_info}\n"
        except Exception:
            pass

    llm = ChatOpenAI(
        model=_MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0.15,
    )

    prompt = user_text
    if git_context:
        prompt = f"{git_context}\n{user_text}"

    response = await llm.ainvoke([
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=prompt),
    ])

    return {"agent_outputs": {"coder": response.content}}


def _last_user_message(messages: list) -> str:
    for msg in reversed(messages):
        if msg.type == "human":
            return msg.content if isinstance(msg.content, str) else ""
    return ""
