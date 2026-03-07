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
_skills_cache: dict[str, str] = {}   # name → full content
_skills_meta: dict[str, str] = {}    # name → description text
_SKILLS_DIR = Path("/app/pipelines/skills")

# Mots vides FR + EN ignorés lors du matching
_STOPWORDS = {
    "a", "an", "the", "is", "in", "to", "how", "do", "can", "me", "i", "for", "of",
    "with", "this", "my", "any", "and", "or", "it", "that", "on", "what", "use",
    "get", "have", "be", "are", "was", "will", "by", "at", "as", "from", "make",
    "build", "show", "give", "let", "want", "need", "please", "help",
    # FR
    "de", "du", "le", "la", "les", "un", "une", "des", "je", "tu", "il", "nous",
    "vous", "ils", "mon", "ma", "mes", "ton", "ta", "tes", "son", "sa", "ses",
    "que", "qui", "quoi", "quel", "quelle", "faire", "fait", "fais", "avec",
    "sans", "mais", "ou", "et", "si", "car", "est", "sur", "par", "pour", "dans",
    "ce", "cet", "ces", "moi", "toi", "lui", "suis", "veux", "peux", "dois",
    "crée", "crée-moi", "génère", "fais-moi", "affiche",
}


def _load_skills() -> None:
    """Charge tous les fichiers skills/*.md dans le cache (appelé une fois)."""
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
    """Retourne les skills les plus pertinents pour la query, scorés par nom + description."""
    _load_skills()
    query_lower = query.lower()
    query_words = {w for w in re.split(r"\W+", query_lower) if len(w) > 3 and w not in _STOPWORDS}

    scored: list[tuple[int, str, str]] = []
    for name, content in _skills_cache.items():
        score = 0
        name_lower = name.lower()

        # Correspondance exacte sur le nom du skill
        if name_lower in query_lower:
            score += 10
        else:
            # Correspondance sur les parties du nom (ex: "three" dans "threejs-3d")
            for part in re.split(r"[-_.]", name_lower):
                if len(part) > 3 and part in query_lower:
                    score += 5

        # Correspondance sur la description (mots-clés significatifs)
        desc = _skills_meta.get(name, "").lower()
        if desc and query_words:
            matches = sum(1 for w in query_words if w in desc)
            score += min(matches, 5)  # cap à 5 pour éviter la surpondération

        if score > 0:
            scored.append((score, name, content))

    scored.sort(key=lambda x: x[0], reverse=True)
    return "\n\n".join(f"### Skill: {n}\n{c[:2000]}" for _, n, c in scored[:2])


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
