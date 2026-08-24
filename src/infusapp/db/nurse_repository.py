from sqlite3 import Row

class NurseRepository:
    def __init__(self, db):
        self.db = db

    def search_by_input(self, user_input: str) -> Row | None:
        return self.db.fetchone(
            (
                "SELECT nurse_id, nurse_name, hash_pw FROM nurses WHERE nurse_id = ? OR nurse_name = ?"
            ),
            (user_input, user_input),
        )

    def add_to_db(self, nurse_id: int, nurse_name: str, hash_pw: str) -> Row | None:
        self.db.execute(
            ("""
                    INSERT INTO nurses (nurse_id, nurse_name, hash_pw)
                    VALUES (?, ?, ?)
                    """),
            (nurse_id, nurse_name, hash_pw),
        )
        return self.db.fetchone(
            ("SELECT nurse_id, nurse_name FROM nurses where nurse_id = ?"),
            (nurse_id,),
        )
