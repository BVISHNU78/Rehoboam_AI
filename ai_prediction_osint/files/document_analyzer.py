from __future__ import annotations

from pathlib import Path

from docx import Document


def analyze_docx(path: str) -> dict:
    document = Document(path)
    text = "\n".join(paragraph.text for paragraph in document.paragraphs if paragraph.text.strip())
    return {
        "path": str(Path(path).resolve()),
        "type": "docx",
        "text": text.strip(),
    }


def analyze_txt(path: str) -> dict:
    text = Path(path).read_text(encoding="utf-8", errors="ignore")
    return {
        "path": str(Path(path).resolve()),
        "type": "txt",
        "text": text.strip(),
    }
