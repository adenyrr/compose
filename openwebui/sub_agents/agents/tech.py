"""
Tech Agent — assistant technique spécialisé.
Modèle : kimi-k2.5.
Outils :
  - Context7 cloud (docs officielles de bibliothèques, frameworks)
  - open-terminal (bash)
  - Skills locaux (skills/*.md) — chargés une fois au démarrage

Le Tech Agent est invoqué pour les questions liées à :
  - l'utilisation de librairies / frameworks spécifiques
  - la documentation technique (API, SDK, config)
  - l'exécution de commandes système dans le terminal
  - les artefacts nécessitant une connaissance approfondie d'une lib spécifique
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import TYPE_CHECKING

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from tools.context7_client import get_library_docs, resolve_library_id
from tools.terminal_client import execute

if TYPE_CHECKING:
    from graph.state import AlyxState

_MODEL = "openrouter/kimi-k2.5"
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")

_SYSTEM = """\
You are a senior technical assistant specializing in libraries, frameworks, and developer tooling.
You have access to:
  1. Official library documentation via Context7
  2. A bash terminal for running commands, checking versions, testing snippets
  3. Local skill files with curated usage guides

When answering:
  - Always consult Context7 docs for the specific library if mentioned
  - Use the terminal to validate commands or check the environment
  - Reference skill files when they provide relevant patterns
  - Reply in English with precise, actionable information
  - For code, use appropriate fenced blocks (```html, ```javascript, ```python, ```bash)
"""

# Cache des skills chargés au démarrage
_skills_cache: dict[str, str] = {}
_SKILLS_DIR = Path("/app/pipelines/skills")


def _load_skills() -> None:
    """Charge tous les fichiers skills/*.md dans le cache (appelé une fois)."""
    if _skills_cache or not _SKILLS_DIR.exists():
        return
    for skill_file in _SKILLS_DIR.glob("*.md"):
        try:
            content = skill_file.read_text(encoding="utf-8")
            # Extraire le name du frontmatter si présent
            name_match = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)
            key = name_match.group(1).strip() if name_match else skill_file.stem
            _skills_cache[key] = content
        except Exception:
            pass


def _find_relevant_skills(query: str) -> str:
    """Retourne le contenu des skills dont le nom ou la description correspond à la query."""
    _load_skills()
    query_lower = query.lower()
    relevant = []
    for name, content in _skills_cache.items():
        # Correspondance sur le nom du skill ou les 3 premières lignes
        header = "\n".join(content.split("\n")[:5]).lower()
        if name.lower() in query_lower or any(word in header for word in query_lower.split()):
            relevant.append(f"### Skill: {name}\n{content[:2000]}")
    return "\n\n".join(relevant[:2])  # Max 2 skills pour ne pas saturer le contexte


async def run(state: "AlyxState", model: str | None = None) -> dict:
    _load_skills()
    messages = state.get("messages", [])
    user_text = _last_user_message(messages)

    context_parts: list[str] = []

    # 1. Skills locaux pertinents
    skill_context = _find_relevant_skills(user_text)
    if skill_context:
        context_parts.append(f"## Relevant local skills\n{skill_context}")

    # 2. Docs Context7 si une librairie est mentionnée
    lib_docs = await _fetch_context7(user_text)
    if lib_docs:
        context_parts.append(f"## Context7 documentation\n{lib_docs}")

    # 3. Commande terminal si utile (vérification d'environnement, version, test)
    terminal_output = ""
    if any(kw in user_text.lower() for kw in ["version", "install", "run", "execute", "check", "test", "terminal", "bash", "shell"]):
        try:
            cmd = _infer_quick_command(user_text)
            if cmd:
                terminal_output = await execute(cmd)
                context_parts.append(f"## Terminal output (`{cmd}`)\n```\n{terminal_output}\n```")
        except Exception as exc:
            context_parts.append(f"## Terminal (unavailable)\n{exc}")

    context = "\n\n".join(context_parts)
    llm = ChatOpenAI(
        model=model or _MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0.15,
    )

    prompt = f"{context}\n\nUser question: {user_text}" if context else user_text
    response = await llm.ainvoke([
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=prompt),
    ])

    return {"agent_outputs": {"tech": response.content}}


async def _fetch_context7(query: str) -> str:
    """
    Détecte les noms de bibliothèques dans la query et récupère leur doc Context7.
    Retourne les docs de la première bibliothèque reconnue.
    """
    # Bibliothèques populaires à détecter heuristiquement
    known_libs = [
        "leaflet", "react", "vue", "angular", "svelte", "tailwind", "bulma",
        "chartjs", "d3", "plotly", "three.js", "threejs", "p5js", "p5",
        "langchain", "langgraph", "fastapi", "django", "flask", "sqlalchemy",
        "pandas", "numpy", "scipy", "sklearn", "tensorflow", "pytorch",
        "docker", "kubernetes", "terraform", "ansible",
        "shadcn", "gsap", "anime.js", "animejs", "konva", "jointjs",
        "mermaid", "vis-network", "vis-timeline", "tabulator",
        "recharts", "reveal.js", "mathjax", "prism", "tone.js",
        "fullcalendar", "leaflet",
    ]
    query_lower = query.lower()
    detected = next((lib for lib in known_libs if lib.replace(".", "").replace("-", "") in query_lower.replace(".", "").replace("-", "")), None)
    if not detected:
        return ""
    try:
        lib_id = await resolve_library_id(detected)
        if not lib_id or "error" in lib_id.lower():
            return ""
        # Extraire un topic de la query (mots clés après le nom de lib)
        topic = query_lower.replace(detected, "").strip()[:80]
        docs = await get_library_docs(lib_id, topic=topic, tokens=4000)
        return docs
    except Exception:
        return ""


def _infer_quick_command(query: str) -> str:
    """Infère une commande shell rapide d'inspection depuis la query."""
    q = query.lower()
    if "python" in q and "version" in q:
        return "python3 --version"
    if "node" in q and "version" in q:
        return "node --version"
    if "docker" in q:
        return "docker --version"
    return ""


def _last_user_message(messages: list) -> str:
    for msg in reversed(messages):
        if msg.type == "human":
            return msg.content if isinstance(msg.content, str) else ""
    return ""
