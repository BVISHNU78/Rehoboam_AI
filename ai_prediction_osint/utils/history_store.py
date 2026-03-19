from __future__ import annotations

import sqlite3
from pathlib import Path


class HistoryStore:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _initialize(self) -> None:
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS prediction_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt TEXT NOT NULL,
                    report TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            connection.commit()

    def save_record(self, prompt: str, report: str) -> None:
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                "INSERT INTO prediction_history (prompt, report) VALUES (?, ?)",
                (prompt, report),
            )
            connection.commit()

    def fetch_records(self, limit: int = 20) -> list[tuple[str, str, str]]:
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.execute(
                """
                SELECT created_at, prompt, report
                FROM prediction_history
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (limit,),
            )
            return cursor.fetchall()
