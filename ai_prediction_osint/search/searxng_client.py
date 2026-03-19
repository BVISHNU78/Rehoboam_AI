from __future__ import annotations

from urllib.parse import urlencode

import requests

from ai_prediction_osint import config
from ai_prediction_osint.utils.logger import get_logger

LOGGER = get_logger(__name__)


class SearXNGClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def search(self, query: str) -> list[dict]:
        params = {"q": query, "format": "json"}
        url = f"{self.base_url}/search?{urlencode(params)}"
        try:
            response = requests.get(url, timeout=config.SEARXNG_TIMEOUT)
            print("SEARX RAW:", response.text)
            response.raise_for_status()
            payload = response.json()
        except requests.RequestException as exc:
            LOGGER.warning("SearXNG request failed for query '%s': %s", query, exc)
            return []
        except ValueError as exc:
            LOGGER.warning("Invalid JSON from SearXNG for query '%s': %s", query, exc)
            return []

        results = []
        for item in payload.get("results", [])[: config.MAX_SEARCH_RESULTS]:
            results.append(
                {
                    "query": query,
                    "title": item.get("title", "Untitled result"),
                    "snippet": item.get("content", "No snippet available."),
                    "url": item.get("url", ""),
                }
            )
        return results

    def deep_search(self, queries: list[str]) -> list[dict]:
        aggregated = []
        seen = set()
        for query in queries:
            for item in self.search(query):
                identity = item.get("url") or f"{item['title']}::{item['snippet']}"
                if identity in seen:
                    continue
                seen.add(identity)
                aggregated.append(item)
        return aggregated
