from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

APP_NAME = "Rehoboam AI"
WINDOW_SIZE = "1000x650"
THEME_MODE = "dark"
COLOR_THEME = "dark-blue"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = DATA_DIR / "cache"
HISTORY_DB_PATH = DATA_DIR / "history.db"

PROJECT_ROOT = BASE_DIR.parent
load_dotenv(PROJECT_ROOT / ".env")

SEARXNG_BASE_URL = os.getenv("SEARXNG_BASE_URL", "https://searx.tiekoetter.com").strip()
SEARXNG_TIMEOUT = 12
MAX_SEARCH_RESULTS = 5
MAX_DEEP_QUERIES = 4

AI_PROVIDER = os.getenv("AI_PROVIDER", "heuristic").strip().lower()
AI_MODEL = os.getenv("AI_MODEL", "heuristic-forecast-v1").strip()
AI_API_URL = os.getenv("AI_API_URL", "").strip()
AI_API_KEY = os.getenv("AI_API_KEY", "").strip()
AI_TIMEOUT = int(os.getenv("AI_TIMEOUT", "45"))
AI_TEMPERATURE = float(os.getenv("AI_TEMPERATURE", "0.3"))

SUPPORTED_FILE_TYPES = {".pdf", ".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".docx", ".txt"}

INTENT_HINTS = {
    "forecast": "prediction",
    "predict": "prediction",
    "future": "prediction",
    "trend": "trend-analysis",
    "risk": "risk-analysis",
    "policy": "policy-analysis",
    "market": "market-analysis",
}

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "how",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "what",
    "when",
    "where",
    "will",
    "with",
}

SPELLING_VOCABULARY = {
    "adoption",
    "analysis",
    "analyst",
    "artificial",
    "automation",
    "chatbot",
    "climate",
    "company",
    "conflict",
    "cyber",
    "data",
    "document",
    "economy",
    "energy",
    "evidence",
    "file",
    "finance",
    "forecast",
    "future",
    "global",
    "government",
    "growth",
    "health",
    "image",
    "impact",
    "industry",
    "intelligence",
    "investment",
    "keyword",
    "market",
    "medical",
    "model",
    "opinion",
    "outcome",
    "pdf",
    "policy",
    "predict",
    "prediction",
    "prompt",
    "regulation",
    "renewable",
    "report",
    "research",
    "result",
    "risk",
    "scenario",
    "search",
    "signal",
    "society",
    "strategy",
    "supply",
    "technical",
    "technology",
    "text",
    "topic",
    "trend",
}
