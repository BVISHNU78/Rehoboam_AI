from __future__ import annotations

from pathlib import Path

import pdfplumber


def analyze_pdf(path: str) -> dict:
    text_chunks = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            if text:
                text_chunks.append(text)

    return {
        "path": str(Path(path).resolve()),
        "type": "pdf",
        "text": "\n".join(text_chunks).strip(),
    }
