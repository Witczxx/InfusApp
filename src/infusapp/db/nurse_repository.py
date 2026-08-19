from sqlite3 import Row

from infusapp.db.connection import Database


class NurseRepository:
    def __init__(self, db: Database):
        self.db = db

    def search_by_input(self, user_input: str) -> Row | None:
        return self.db.fetchone(
            (
                "SELECT nurse_id, nurse_name, pw FROM nurses WHERE nurse_id = ? OR nurse_name = ?"
            ),
            (user_input, user_input),
        )
