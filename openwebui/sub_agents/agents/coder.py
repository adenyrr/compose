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
import re
from pathlib import Path
from typing import TYPE_CHECKING

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from tools.mcpo_client import call_tool

if TYPE_CHECKING:
    from graph.state import AlyxState

_MODEL = "openrouter/kimi-k2.5"
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")

# ------- Skills (même système que tech.py) -------
_skills_cache: dict[str, str] = {}
_skills_meta: dict[str, str] = {}
_SKILLS_DIR = Path("/app/pipelines/skills")

_STOPWORDS = {
    "a", "an", "the", "is", "in", "to", "how", "do", "can", "me", "i", "for", "of",
    "with", "this", "my", "any", "and", "or", "it", "that", "on", "what", "use",
    "get", "have", "be", "are", "was", "will", "by", "at", "as", "from", "make",
    "build", "show", "give", "let", "want", "need", "please", "help", "write", "create",
    "de", "du", "le", "la", "les", "un", "une", "des", "je", "tu", "il", "nous",
    "vous", "ils", "mon", "ma", "mes", "ton", "ta", "tes", "son", "sa", "ses",
    "que", "qui", "quoi", "quel", "quelle", "faire", "fait", "fais", "avec",
    "sans", "mais", "ou", "et", "si", "car", "est", "sur", "par", "pour", "dans",
    "ce", "cet", "ces", "moi", "toi", "lui", "suis", "veux", "peux", "dois",
    "crée", "crée-moi", "génère", "fais-moi", "affiche",
}


def _load_skills() -> None:
    if _skills_cache or not _SKILLS_DIR.exists():
        return
    for skill_file in _SKILLS_DIR.glob("*.md"):
        try:
            content = skill_file.read_text(encoding="utf-8")
            name_match = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)
            key = name_match.group(1).strip() if name_match else skill_file.stem
            desc_match = re.search(r"^description:\s*(.+)$", content, re.MULTILINE)
            _skills_cache[key] = content
            _skills_meta[key] = desc_match.group(1).strip() if desc_match else ""
        except Exception:
            pass


def _find_relevant_skills(query: str) -> str:
    _load_skills()
    query_lower = query.lower()
    query_words = {w for w in re.split(r"\W+", query_lower) if len(w) > 3 and w not in _STOPWORDS}
    scored: list[tuple[int, str, str]] = []
    for name, content in _skills_cache.items():
        score = 0
        name_lower = name.lower()
        if name_lower in query_lower:
            score += 10
        else:
            for part in re.split(r"[-_.]", name_lower):
                if len(part) > 3 and part in query_lower:
                    score += 5
        desc = _skills_meta.get(name, "").lower()
        if desc and query_words:
            score += min(sum(1 for w in query_words if w in desc), 5)
        if score > 0:
            scored.append((score, name, content))
    scored.sort(key=lambda x: x[0], reverse=True)
    return "\n\n".join(f"### Skill: {n}\n{c[:2000]}" for _, n, c in scored[:2])

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


async def run(state: "AlyxState", model: str | None = None) -> dict:
    _load_skills()
    messages = state.get("messages", [])
    user_text = _last_user_message(messages)

    context_parts: list[str] = []

    # 1. Skills pertinents
    skill_context = _find_relevant_skills(user_text)
    if skill_context:
        context_parts.append(f"## Relevant skills\n{skill_context}")

    # 2. Contexte git si pertinent
    if any(kw in user_text.lower() for kw in ["git", "commit", "diff", "branch", "repo"]):
        try:
            git_info = await call_tool("git", "git_status", {})
            context_parts.append(f"## Git status\n{git_info}")
        except Exception:
            pass

    llm = ChatOpenAI(
        model=model or _MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0.15,
    )

    context = "\n\n".join(context_parts)
    prompt = f"{context}\n\nUser request: {user_text}" if context else user_text

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
