from __future__ import annotations


def format_prediction_report(analysis: dict, model_output: dict, reasoning: dict) -> str:
    lines = [
        "Rehoboam AI Report",
        "",
        f"Topic: {model_output['topic']}",
        f"Intent: {analysis.get('intent', 'general-analysis')}",
        f"Confidence: {model_output['confidence']}%",
        "",
        "Signals detected:",
    ]
    lines.extend(f"- {signal}" for signal in reasoning.get("signals", []))
    lines.extend(
        [
            "",
            "AI Opinion:",
            model_output["opinion"],
            "",
            "Possible outcomes:",
        ]
    )
    lines.extend(f"- {label} ({probability}%)" for label, probability in model_output["outcomes"])

    evidence = reasoning.get("evidence", [])
    if evidence:
        lines.extend(["", "Supporting evidence samples:"])
        lines.extend(f"- {item}" for item in evidence[:4])

    return "\n".join(lines)
