from __future__ import annotations

from collections import Counter

from ai_prediction_osint.utils.text_processing import extract_keywords, sentiment_signal


class ReasoningEngine:
    def build_signals(self, prompt: str, web_data: list[dict], file_data: list[dict]) -> dict:
        signal_counter: Counter[str] = Counter()
        evidence: list[str] = []

        for keyword in extract_keywords(prompt):
            signal_counter[f"persistent attention around {keyword}"] += 1

        for item in web_data:
            combined = f"{item.get('title', '')} {item.get('snippet', '')}".strip()
            if not combined:
                continue
            mood = sentiment_signal(combined)
            signal_counter[mood] += 1
            for keyword in extract_keywords(combined)[:3]:
                signal_counter[f"repeated signal: {keyword}"] += 1
            evidence.append(combined[:180])

        for item in file_data:
            extracted = item.get("text", "")
            if extracted:
                signal_counter["supporting evidence from uploaded files"] += 1
                for keyword in extract_keywords(extracted)[:3]:
                    signal_counter[f"file-backed signal: {keyword}"] += 1
                evidence.append(extracted[:180])

        return {
            "signals": [signal for signal, _ in signal_counter.most_common(6)] or ["limited intelligence available"],
            "evidence": evidence[:6],
        }
