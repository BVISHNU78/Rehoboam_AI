from __future__ import annotations

from pathlib import Path

import pytesseract
from PIL import Image


def analyze_image(path: str) -> dict:
    image = Image.open(path)
    text = pytesseract.image_to_string(image)
    return {
        "path": str(Path(path).resolve()),
        "type": "image",
        "text": text.strip(),
    }
