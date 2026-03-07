"""
Supervisor Node — classification de l'intent utilisateur.

Utilise GPT-OSS 120B pour analyser le dernier message et retourner
la liste des agents à invoquer pour ce tour. Répond en JSON pur.

Agents disponibles :
  vision        — images, OCR, screenshots, analyse visuelle
  scholar       — articles scientifiques, recherche académique, littérature
  dev           — code, artifacts interactifs (html/js), questions techniques,
                  docs de bibliothèques/frameworks, bash, visualisation de données
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
    "vision", "scholar", "dev", "web",
    "media", "data", "memory", "image_gen", "rag",
}

_SYSTEM = """\
You are a routing classifier for a multi-agent AI system.
Given the user's last message (and whether images are attached), output ONLY a JSON array
of agent names to invoke. No explanation, no markdown — just the JSON array.

Agent catalog:
  "vision"     → images present, or requests about image content/OCR
  "scholar"    → scientific papers, academic research, citations, studies
  "dev"        → writing code, creating interactive artifacts (HTML/JS/Python), technical
                 questions about libraries/frameworks, bash commands, git operations,
                 data formatting/display/visualization, ANY output that should be visual
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
  - Use "dev" for ALL code generation, artifact creation, data formatting/display, and library questions.
  - Use "data" ONLY for pure math/statistics/SQL with no display requirement.
  - When data needs to be DISPLAYED or FORMATTED, use "dev" (not "data").
  - CRITICAL — web + dev parallelism: agents run IN PARALLEL and cannot share data within the same
    turn. NEVER combine ["web", "dev"] when the user wants to fetch data AND then visualize it —
    dev would run without web's results. Instead:
    • If the user wants data fetched + visualized: route to ["web"] ONLY.
      Alyx will present the data as text; the user can ask for visualization on the next turn.
    • ["dev"] alone is correct when the user already has the data in the conversation or provides it.
    • ["web", "dev"] is only valid when dev's task is INDEPENDENT of what web fetches
      (e.g., "search for the latest news AND write a Python hello world").

Examples:
  "What studies exist on working memory?" → ["scholar"]
  "Write a Python script to parse JSON" → ["dev"]
  "Écris moi un script Python pour parser du JSON" → ["dev"]
  "Create an interactive bubble chart" → ["dev"]
  "Fais moi un graphique de données interactif" → ["dev"]
  "Mets ces données en forme" → ["dev"]
  "Affiche ces résultats dans un tableau" → ["dev"]
  "Présente ces statistiques visuellement" → ["dev"]
  "Create a 3D spinning cube with Three.js" → ["dev"]
  "Crée moi une visualisation 3D avec Three.js" → ["dev"]
  "Build a dashboard with Chart.js" → ["dev"]
  "Construis un dashboard avec Chart.js" → ["dev"]
  "How do I use the Leaflet.js clustering plugin?" → ["dev"]
  "How does React's useEffect hook work?" → ["dev"]
  "Comment puis-je utiliser React Router?" → ["dev"]
  "Debug this Python traceback: ..." → ["dev"]
  "Summarize this YouTube video: https://..." → ["media"]
  "Generate a misty forest image" → ["image_gen"]
  "[image attached] What's in this chart?" → ["vision"]
  "Calculate compound interest at 5% over 10 years" → ["data"]
  "What is the result of (12 * 4) + 7?" → ["data"]
  "What do you remember about my research?" → ["memory"]
  "Search for recent news about LLMs" → ["web"]
  "Cherche les coordonnées de chute des missiles nord-coréens" → ["web"]
  "Récupère les données sur les tremblements de terre et fais une carte" → ["web"]
  "Cherche des données sur X et crée un graphique" → ["web"]
  "Search for X data and plot it" → ["web"]
  "What does my uploaded report say about Q3?" → ["rag"]
  "Hello, how are you?" → []
  "Bonjour, comment vas-tu ?" → []
"""


async def route(state: "AlyxState", model: str | None = None) -> "AlyxState":
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
    date_note = f"\n[Today: {state.get('current_date', '')}]" if state.get("current_date") else ""
    routing_prompt = f"{user_text}{images_note}{date_note}"

    llm = ChatOpenAI(
        model=model or _MODEL,
        base_url=_LITELLM_URL,
        api_key=_LITELLM_API_KEY,
        temperature=0,
        max_tokens=128,
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
