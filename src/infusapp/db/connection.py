import sqlite3

from contextlib import contextmanager
from pathlib import Path

class Database:
    def __init__(self, db_path: Path):
        self.db_path = db_path

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row      # Assess rows by header instead of number
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def execute(self, query: str, params: tuple = ()) -> None:      # Empty Tuple if no Value
        with self.get_connection() as conn:
            conn.execute(query, params)

    def executemany(self, query: str, params_list: list[tuple]) -> None:
        with self.get_connection() as conn:
            conn.executemany(query, params_list)

    def fetchone(self, query: str, params: tuple = ()) -> sqlite3.Row | None:
        with self.get_connection() as conn:
            conn.execute(query, params).fetchone()

    def fetch_all(self, query: str, params: tuple = ()) -> list[sqlite3.Row] | None:
        with self.get_connection() as conn:
            return conn.execute(query, params).fetchall()
