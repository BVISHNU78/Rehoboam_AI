from __future__ import annotations

import customtkinter as ctk


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, on_select) -> None:
        super().__init__(master, width=180, corner_radius=0)
        self.grid_rowconfigure(5, weight=1)
        self._on_select = on_select

        self.title_label = ctk.CTkLabel(
            self,
            text="Rehoboam\nAI",
            font=ctk.CTkFont(size=22, weight="bold"),
            justify="left",
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(24, 18), sticky="w")

        options = [
            ("Predict Future", "predict"),
            ("Intelligence Search", "intelligence"),
            ("History", "history"),
            ("Settings", "settings"),
        ]
        self.buttons = {}
        for index, (label, key) in enumerate(options, start=1):
            button = ctk.CTkButton(
                self,
                text=label,
                anchor="w",
                height=42,
                command=lambda item=key: self.select(item),
            )
            button.grid(row=index, column=0, padx=16, pady=8, sticky="ew")
            self.buttons[key] = button

        self.set_active("predict")

    def select(self, key: str) -> None:
        self.set_active(key)
        self._on_select(key)

    def set_active(self, key: str) -> None:
        for name, button in self.buttons.items():
            button.configure(fg_color=("#1f538d" if name == key else "#2b2b2b"))
