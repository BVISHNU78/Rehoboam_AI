from __future__ import annotations

import difflib
import re

from ai_prediction_osint import config


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def first_sentence(text: str) -> str:
    match = re.split(r"[.!?\n]", text.strip(), maxsplit=1)
    return match[0].strip() if match else ""


def extract_keywords(text: str) -> list[str]:
    candidates = re.findall(r"[A-Za-z][A-Za-z\-]{2,}", text.lower())
    keywords = []
    seen = set()
    for word in candidates:
        if word in config.STOPWORDS or word in seen:
            continue
        seen.add(word)
        keywords.append(word)
    return keywords


def correct_spelling(text: str) -> tuple[str, list[tuple[str, str]]]:
    vocabulary = config.STOPWORDS | config.SPELLING_VOCABULARY
    corrections: list[tuple[str, str]] = []

    def replace(match: re.Match[str]) -> str:
        token = match.group(0)
        lower_token = token.lower()
        if len(token) < 4 or lower_token in vocabulary:
            return token
        if re.search(r"\d", token) or "://" in token or "." in token:
            return token

        suggestion = difflib.get_close_matches(lower_token, list(vocabulary), n=1, cutoff=0.84)
        if not suggestion or suggestion[0] == lower_token:
            return token

        corrected = suggestion[0]
        if token[0].isupper():
            corrected = corrected.capitalize()
        corrections.append((token, corrected))
        return corrected

    corrected_text = re.sub(r"\b[A-Za-z][A-Za-z\-]{2,}\b", replace, text)
    return corrected_text, corrections


def sentiment_signal(text: str) -> str:
    lowered = text.lower()
    positive_terms = ("growth", "increase", "investment", "adoption", "expansion", "breakthrough")
    negative_terms = ("risk", "decline", "ban", "slowdown", "conflict", "shortage")

    positive_score = sum(term in lowered for term in positive_terms)
    negative_score = sum(term in lowered for term in negative_terms)

    if positive_score > negative_score:
        return "positive momentum"
    if negative_score > positive_score:
        return "elevated risk pressure"
    return "mixed directional signal"
