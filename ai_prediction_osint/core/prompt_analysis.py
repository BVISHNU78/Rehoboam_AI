from __future__ import annotations

from ai_prediction_osint import config
from ai_prediction_osint.utils.text_processing import correct_spelling, extract_keywords, first_sentence, normalize_text


def analyze_prompt(prompt: str) -> dict:
    corrected_prompt, corrections = correct_spelling(prompt)
    cleaned_prompt = normalize_text(corrected_prompt)
    keywords = extract_keywords(cleaned_prompt)
    topic = first_sentence(corrected_prompt) or "General Intelligence Topic"

    intent = "general-analysis"
    lowered = cleaned_prompt.lower()
    for hint, resolved_intent in config.INTENT_HINTS.items():
        if hint in lowered:
            intent = resolved_intent
            break

    needs_file_context = any(word in lowered for word in ("report", "document", "image", "pdf", "evidence", "file"))
    if any(word in lowered for word in ("financial", "contract", "medical", "technical")):
        needs_file_context = True

    return {
        "topic": topic[:120],
        "keywords": keywords[:10],
        "intent": intent,
        "needs_file_context": needs_file_context,
        "corrected_prompt": corrected_prompt,
        "corrections": corrections,
    }
