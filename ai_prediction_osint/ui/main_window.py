from __future__ import annotations

import threading
from tkinter import filedialog, messagebox

import customtkinter as ctk

from ai_prediction_osint import config
from ai_prediction_osint.core.prompt_analysis import analyze_prompt
from ai_prediction_osint.core.prediction_engine import generate_prediction
from ai_prediction_osint.files.file_manager import FileManager
from ai_prediction_osint.search.deep_search import build_deep_search_queries
from ai_prediction_osint.search.searxng_client import SearXNGClient
from ai_prediction_osint.ui.panels import ChatPanel, StatusPanel
from ai_prediction_osint.utils.history_store import HistoryStore
from ai_prediction_osint.utils.logger import get_logger

LOGGER = get_logger(__name__)


class MainWindow(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        ctk.set_appearance_mode(config.THEME_MODE)
        ctk.set_default_color_theme(config.COLOR_THEME)

        self.title(config.APP_NAME)
        self.geometry(config.WINDOW_SIZE)
        self.minsize(820, 560)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.analysis = {}
        self.web_data = []
        self.file_data = []

        self.history_store = HistoryStore(config.HISTORY_DB_PATH)
        self.file_manager = FileManager()
        self.searxng_client = SearXNGClient(config.SEARXNG_BASE_URL)

        self.content = ctk.CTkFrame(self)
        self.content.grid(row=0, column=0, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=0)

        self.chat_panel = ChatPanel(self.content, on_send=self.on_predict_future, on_upload=self.on_upload_file)
        self.chat_panel.grid(row=0, column=0, sticky="nsew")

        self.status_panel = StatusPanel(self.content)
        self.status_panel.grid(row=1, column=0, sticky="ew")

    def on_predict_future(self) -> None:
        prompt = self.chat_panel.get_prompt()
        if not prompt or prompt == "Type your prompt here...":
            messagebox.showwarning("Missing prompt", "Enter a prompt before generating predictions.")
            return
        self.chat_panel.append_message("You", prompt)
        self.chat_panel.clear_prompt()
        self._run_thread(self._predict_worker, prompt)

    def on_upload_file(self) -> None:
        paths = filedialog.askopenfilenames(
            title="Select supporting files",
            filetypes=[
                ("Supported files", "*.pdf *.png *.jpg *.jpeg *.bmp *.tiff *.docx *.txt"),
                ("All files", "*.*"),
            ],
        )
        if not paths:
            return
        self.status_panel.set_status("Analyzing uploaded files...", 0.1)
        self._run_thread(self._file_worker, list(paths))

    def _run_thread(self, target, *args) -> None:
        thread = threading.Thread(target=target, args=args, daemon=True)
        thread.start()

    def _predict_worker(self, prompt: str) -> None:
        self._set_status_async("Analyzing prompt...", 0.15)
        analysis = analyze_prompt(prompt)
        self.analysis = analysis
        corrected_prompt = analysis.get("corrected_prompt", prompt)

        self._set_status_async("Collecting intelligence...", 0.45)
        queries = build_deep_search_queries(corrected_prompt, analysis)
        self.web_data = self.searxng_client.deep_search(queries)

        self._set_status_async("Generating response...", 0.8)
        report = generate_prediction(corrected_prompt, self.web_data, self.file_data)
        response = self._compose_chat_response(analysis, report, len(self.web_data))
        self.after(0, lambda: self.chat_panel.append_message("Assistant", response))
        self.history_store.save_record(corrected_prompt, report)
        self._set_status_async("Completed.", 1.0)

    def _file_worker(self, paths: list[str]) -> None:
        file_data = self.file_manager.analyze_files(paths)
        self.file_data.extend(file_data)
        uploaded_names = "\n".join(f"- {item.get('path', '')}" for item in file_data) or "- No readable files"
        message = f"I loaded these files and will use them in the next prediction:\n{uploaded_names}"
        self.after(0, lambda: self.chat_panel.append_message("Assistant", message))
        self._set_status_async(f"Loaded {len(file_data)} file analyses.", 0.35)

    def _compose_chat_response(self, analysis: dict, report: str, web_count: int) -> str:
        summary = [
            f"Topic: {analysis.get('topic', 'Unknown')}",
            f"Intent: {analysis.get('intent', 'general-analysis')}",
            f"Search results used: {web_count}",
            f"Uploaded files used: {len(self.file_data)}",
        ]
        corrections = analysis.get("corrections", [])
        if corrections:
            summary.append("Spell correction applied:")
            summary.extend(f"- {original} -> {corrected}" for original, corrected in corrections[:6])
        summary.extend(
            [
                "",
            report,
            ]
        )
        return "\n".join(summary)

    def _set_status_async(self, text: str, progress: float) -> None:
        self.after(0, lambda: self.status_panel.set_status(text, progress))


def run_app() -> None:
    LOGGER.info("Starting %s", config.APP_NAME)
    app = MainWindow()
    app.mainloop()
