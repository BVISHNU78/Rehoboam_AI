from __future__ import annotations

from ai_prediction_osint import config


def build_deep_search_queries(prompt: str, analysis: dict) -> list[str]:
    topic = analysis.get("topic", prompt).strip()
    keywords = analysis.get("keywords", [])

    templates = [
        topic,
        f"{topic} latest developments",
        f"{topic} forecast",
        f"{topic} risks and opportunities",
    ]

    if keywords:
        templates.append(f"{' '.join(keywords[:3])} trends")
        templates.append(f"{keywords[0]} news")

    unique = []
    seen = set()
    for query in templates:
        normalized = query.lower()
        if normalized in seen:
            continue
        seen.add(normalized)
        unique.append(query)
        if len(unique) >= config.MAX_DEEP_QUERIES:
            break
    return unique
