from __future__ import annotations

import customtkinter as ctk


class ChatPanel(ctk.CTkFrame):
    def __init__(self, master, on_send, on_upload) -> None:
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkLabel(self, text="Rehoboam AI", font=ctk.CTkFont(size=24, weight="bold"))
        header.grid(row=0, column=0, padx=20, pady=(18, 8), sticky="w")

        self.chat_box = ctk.CTkTextbox(self, wrap="word")
        self.chat_box.grid(row=1, column=0, padx=20, pady=(0, 12), sticky="nsew")
        self.chat_box.insert(
            "1.0",
            "Assistant:\nAsk a question about the future, trends, risks, or a topic you want analyzed.\n\n",
        )
        self.chat_box.configure(state="disabled")

        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.grid(row=2, column=0, padx=20, pady=(0, 18), sticky="ew")
        controls.grid_columnconfigure(0, weight=1)

        self.prompt_box = ctk.CTkTextbox(controls, height=90)
        self.prompt_box.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.prompt_box.insert("1.0", "Type your prompt here...")

        self.upload_button = ctk.CTkButton(controls, text="Upload PDF/File", command=on_upload, width=150)
        self.upload_button.grid(row=1, column=0, pady=(10, 0), sticky="w")

        self.send_button = ctk.CTkButton(controls, text="Send", command=on_send, width=120)
        self.send_button.grid(row=1, column=1, padx=(10, 0), pady=(10, 0), sticky="e")

    def get_prompt(self) -> str:
        return self.prompt_box.get("1.0", "end").strip()

    def clear_prompt(self) -> None:
        self.prompt_box.delete("1.0", "end")

    def append_message(self, speaker: str, text: str) -> None:
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", f"{speaker}:\n{text.strip()}\n\n")
        self.chat_box.see("end")
        self.chat_box.configure(state="disabled")


class StatusPanel(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, height=42)
        self.grid_columnconfigure(1, weight=1)

        self.status_label = ctk.CTkLabel(self, text="Ready.")
        self.status_label.grid(row=0, column=0, padx=16, pady=10, sticky="w")

        self.progress = ctk.CTkProgressBar(self)
        self.progress.grid(row=0, column=1, padx=16, pady=10, sticky="ew")
        self.progress.set(0)

    def set_status(self, text: str, progress: float | None = None) -> None:
        self.status_label.configure(text=text)
        if progress is not None:
            self.progress.set(progress)
