from sqlite3 import Row


class MediRepository:

    def __init__(self, db):
        self.db = db

    def search_by_input(self, user_input: str | int) -> list[Row]:
        return self.db.fetch_all(
            ("""
                 SELECT ingredient, df, strength, route, trade_name
                 FROM medications WHERE ingredient LIKE '%' || ? || '%'
                 """),
            (user_input,),
        )

    def get_strengths(self, chosen_ingredient: str) -> list[Row]:
        return self.db.fetch_all(
            ("""
                 SELECT strength FROM medications WHERE ingredient = ?
                 """),
            (chosen_ingredient,),
        )

    def search_df(self, chosen_ingredient: str, strength: str) -> list[Row]:
        return self.db.fetch_all(
            ("""
                 SELECT df FROM medications WHERE ingredient = ? AND strength = ?
                 """),
            (
                chosen_ingredient,
                strength,
            ),
        )
