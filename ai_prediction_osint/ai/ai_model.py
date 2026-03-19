from __future__ import annotations

import json
import re
import requests

from ai_prediction_osint import config
from ai_prediction_osint.utils.logger import get_logger

LOGGER = get_logger(__name__)


class AIModel:

    def predict(self, analysis: dict, reasoning: dict, web_data: list[dict], file_data: list[dict]) -> dict:
        if config.AI_PROVIDER == "ollama":
            result = self._predict_ollama(analysis, reasoning, web_data, file_data)
            if result:
                return result

        return self._predict_heuristic(analysis)

    # ================= OLLAMA =================

    def _predict_ollama(self, analysis, reasoning, web_data, file_data):

        api_url = config.AI_API_URL or "http://localhost:11434/api/generate"

        payload = {
            "model": config.AI_MODEL or "qwen2.5:3b",
            "stream": False,
            "options": {
                "temperature": config.AI_TEMPERATURE
            },
            "prompt":
                self._system_prompt()
                + "\n\n"
                + self._build_user_prompt(analysis, reasoning, web_data, file_data),
        }

        try:
            response = requests.post(api_url, json=payload, timeout=config.AI_TIMEOUT)
            response.raise_for_status()

            data = response.json()
            content = data.get("response", "")

            return self._parse_model_response(content, analysis)

        except Exception as e:
            LOGGER.warning("Ollama prediction failed: %s", e)
            return None

    # ================= PROMPTS =================

    def _system_prompt(self) -> str:
        return (
            "You are a geopolitical intelligence analyst.\n"
            "Return ONLY prediction JSON.\n\n"
            "Format:\n"
            "{\n"
            " topic: str\n"
            " confidence: int\n"
            " opinion: str\n"
            " outcomes: [ {label:str, probability:int} x3 ]\n"
            "}"
        )

    def _build_user_prompt(self, analysis, reasoning, web_data, file_data):
        return json.dumps(
            {
                "analysis": analysis,
                "reasoning": reasoning,
                "web": web_data[:5],
                "files": file_data[:3],
            },
            ensure_ascii=False,
        )

    # ================= PARSER =================

    def _parse_model_response(self, content: str, analysis: dict) -> dict:

        # remove markdown fences
        content = re.sub(r"```json|```", "", content)

        parsed = None

        # try direct json parse
        try:
            obj = json.loads(content)

            if "analysis" in obj:
                parsed = obj["analysis"]

            elif "prediction" in obj:
                parsed = obj["prediction"]

            else:
                parsed = obj

        except:
            # fallback → find biggest json block
            matches = re.findall(r'\{.*\}', content, re.DOTALL)

            for m in matches:
                try:
                    obj = json.loads(m)

                    if "analysis" in obj:
                        parsed = obj["analysis"]
                        break

                    if "prediction" in obj:
                        parsed = obj["prediction"]
                        break

                    if "opinion" in obj:
                        parsed = obj

                except:
                    continue

        if not parsed:
            LOGGER.warning("LLM returned non structured output")

            return {
                "topic": analysis.get("topic", "Unknown"),
                "confidence": 60,
                "opinion": content[:800],
                "outcomes": [
                    ("Escalation likely", 40),
                    ("Stalemate", 35),
                    ("De-escalation", 25),
                ],
            }

        outcomes = []

        for item in parsed.get("outcomes", [])[:3]:
            outcomes.append(
                (
                    item.get("label", "Unknown"),
                    int(item.get("probability", 0)),
                )
            )

        return {
            "topic": parsed.get("topic", analysis.get("topic", "Unknown")),
            "confidence": int(parsed.get("confidence", 60)),
            "opinion": parsed.get("opinion", content[:800]),
            "outcomes": outcomes,
        }

    # ================= HEURISTIC =================

    def _predict_heuristic(self, analysis):

        topic = analysis.get("topic", "Unknown")

        return {
            "topic": topic,
            "confidence": 30,
            "opinion": "Insufficient intelligence evidence. Preliminary hypothesis only.",
            "outcomes": [
                ("Escalation likely", 30),
                ("Stalemate", 40),
                ("De-escalation", 30),
            ],
        }