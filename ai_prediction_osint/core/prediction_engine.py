from __future__ import annotations

from ai_prediction_osint.ai.ai_model import AIModel
from ai_prediction_osint.ai.ai_reasoning import format_prediction_report
from ai_prediction_osint.core.prompt_analysis import analyze_prompt
from ai_prediction_osint.core.reasoning_engine import ReasoningEngine


def generate_prediction(prompt: str, web_data: list[dict], file_data: list[dict]) -> str:
    analysis = analyze_prompt(prompt)
    reasoning = ReasoningEngine().build_signals(prompt, web_data, file_data)
    model_output = AIModel().predict(analysis, reasoning, web_data, file_data)
    return format_prediction_report(analysis, model_output, reasoning)
