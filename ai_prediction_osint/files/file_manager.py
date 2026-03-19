from __future__ import annotations

from pathlib import Path

from ai_prediction_osint import config
from ai_prediction_osint.files.document_analyzer import analyze_docx, analyze_txt
from ai_prediction_osint.files.image_analyzer import analyze_image
from ai_prediction_osint.files.pdf_analyzer import analyze_pdf
from ai_prediction_osint.utils.logger import get_logger

LOGGER = get_logger(__name__)


class FileManager:
    def analyze_files(self, paths: list[str]) -> list[dict]:
        results = []
        for raw_path in paths:
            path = Path(raw_path)
            suffix = path.suffix.lower()
            if suffix not in config.SUPPORTED_FILE_TYPES:
                LOGGER.warning("Skipping unsupported file type: %s", raw_path)
                continue
            try:
                if suffix == ".pdf":
                    results.append(analyze_pdf(raw_path))
                elif suffix in {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}:
                    results.append(analyze_image(raw_path))
                elif suffix == ".docx":
                    results.append(analyze_docx(raw_path))
                elif suffix == ".txt":
                    results.append(analyze_txt(raw_path))
            except Exception as exc:  # pragma: no cover
                LOGGER.exception("Failed to analyze file %s: %s", raw_path, exc)
        return results

    def render_summary(self, file_data: list[dict]) -> str:
        if not file_data:
            return "No file data loaded.\n"
        lines = ["Uploaded File Analysis", ""]
        for item in file_data:
            preview = item.get("text", "")[:280] or "No text extracted."
            lines.extend(
                [
                    f"Path: {item.get('path', '')}",
                    f"Type: {item.get('type', 'unknown')}",
                    f"Preview: {preview}",
                    "",
                ]
            )
        return "\n".join(lines).strip()
