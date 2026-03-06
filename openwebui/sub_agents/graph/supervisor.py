"""
Supervisor Node — classification de l'intent utilisateur.

Utilise GPT-OSS 120B pour analyser le dernier message et retourner
la liste des agents à invoquer pour ce tour. Répond en JSON pur.

Agents disponibles :
  vision        — images, OCR, screenshots, analyse visuelle
  scholar       — articles scientifiques, recherche académique, littérature
  coder         — code, scripts, artifacts interactifs (html/js/py), fichiers
  tech          — docs de bibliothèques/frameworks, bash, questions techniques
  web           — navigation web, scraping, recherche d'actualités, URLs
  media         — vidéos YouTube, documents PDF/Word, transcription, conversion
  data          — calculs mathématiques, expressions numériques, SQL/DuckDB
  memory        — informations personnelles, préférences, contexte passé
  image_gen     — génération d'images, illustrations, visuels
  rag           — questions sur les documents uploadés par l'utilisateur
"""

from __future__ import annotations

import json
import os
import re
from typing import TYPE_CHECKING

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

if TYPE_CHECKING:
    from graph.state import AlyxState

_MODEL = "openrouter/gpt-oss"
_LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1")
_LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")

_VALID_AGENTS = {
    "vision", "scholar", "coder", "tech", "web",
    "media", "data", "memory", "image_gen", "rag",
}

_SYSTEM = """\
You are a routing classifier for a multi-agent AI system.
Given the user's last message (and whether images are attached), output ONLY a JSON array
of agent names to invoke. No explanation, no markdown — just the JSON array.

Agent catalog:
  "vision"     → images present, or requests about image content/OCR
  "scholar"    → scientific papers, academic research, citations, studies
  "coder"      → writing code, creating interactive artifacts (HTML/JS/Python), git operations
  "tech"       → using a specific library/framework, technical docs, bash commands
  "web"        → browsing a URL, searching the web, news, current events
  "media"      → YouTube videos, transcripts, PDF/Word documents, format conversion
  "data"       → arithmetic, math calculations, statistics, SQL/DuckDB queries
  "memory"     → recall user preferences or past conversation info
  "image_gen"  → generate an image, illustration, or visual
  "rag"        → questions about documents the user has uploaded

Rules:
  - Return [] (empty array) if the question needs no specialized agent (simple conversational reply).
  - Return at most 3 agents per turn to avoid context bloat.
  - If images are attached, ALWAYS include "vision".
  - "memory" can be combined with any other agent when context recall seems useful.
  - Prefer specialization: "tech" over "coder" when the question is about a specific library.
  - "coder" AND "tech" together only if both code generation AND library docs are needed.

Examples:
  "What studies exist on working memory?" → ["scholar"]
  "Create an interactive bubble chart" → ["coder"]
  "How do I use the Leaflet.js clustering plugin?" → ["tech"]
  "Summarize this YouTube video: https://..." → ["media"]
  "Generate a misty forest image" → ["image_gen"]
  "[image attached] What's in this chart?" → ["vision"]
  "Calculate compound interest at 5% over 10 years" → ["data"]
  "What do you remember about my research?" → ["memory"]
  "Search for recent news about LLMs" → ["web"]
  "What does my uploaded report say about Q3?" → ["rag"]
  "Hello, how are you?" → []
"""


async def route(state: "AlyxState") -> "AlyxState":
    """
    Nœud superviseur — détermine les agents à invoquer et met à jour state['routing'].
    """
    messages = state.get("messages", [])
    images_b64 = state.get("images_b64", [])

    user_text = ""
    for msg in reversed(messages):
        if msg.type == "human":
            user_text = msg.content if isinstance(msg.content, str) else ""
            break

    images_note = f"\n[{len(images_b64)} image(s) attached]" if images_b64 else ""
    routing_prompt = f"{user_text}{images_note}"

    llm = ChatOpenAI(
        model=_MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0,
        max_tokens=64,
    )

    try:
        response = await llm.ainvoke([
            SystemMessage(content=_SYSTEM),
            HumanMessage(content=routing_prompt),
        ])
        raw = response.content.strip()
        # Extraire le JSON array même si le modèle entoure de backticks
        match = re.search(r"\[.*?\]", raw, re.DOTALL)
        if match:
            agents = json.loads(match.group(0))
        else:
            agents = []
        # Filtrer les agents invalides, limiter à 3
        agents = [a for a in agents if a in _VALID_AGENTS][:3]
    except Exception:
        agents = []

    return {**state, "routing": agents, "agent_outputs": {}, "artifacts": []}
