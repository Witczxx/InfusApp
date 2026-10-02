import re
from sqlite3 import Row
from datetime import datetime, timedelta

class MediService:

    def __init__(self, medi_rep):
        self.medi_rep = medi_rep

    def fetch_data(self, user_input) -> list[Row]:
        fetched_data: list[Row] = self.medi_rep.search_by_input(user_input=user_input)
        return fetched_data

    def filter_ingredients_by_route(
        self, user_input: str, fetched_data: list[Row]
    ) -> list | None:
        ingredients_by_route: set = {
            finding["ingredient"]
            for finding in fetched_data
            if ("INTRAVENOUS" in finding["route"] or "INJECTION" in finding["route"])
            and any(user_input in str(string) for string in finding)
        }
        if not ingredients_by_route:
            return None
        return sorted(ingredients_by_route)

    def find_strengths(self, chosen_ingredient) -> list:
        found_strengths: list[Row] = self.medi_rep.get_strengths(
            chosen_ingredient=chosen_ingredient
        )
        unique_strengths = {strength["strength"] for strength in found_strengths}
        return sorted(unique_strengths, key=self.strengths_sort_key)

    def strengths_sort_key(self, strengths) -> tuple:
        matches = re.findall(r"\d+", strengths)
        return tuple(int(n) for n in matches)

    def find_df(self, chosen_ingredient: str, strength: str) -> str:
        df_findings: list[Row] = self.medi_rep.search_df(
            chosen_ingredient=chosen_ingredient, strength=strength
        )
        if df_findings:
            df_findings_set: set = {finding["df"] for finding in df_findings}
            return " | ".join(sorted(df_findings_set))
        else:
            print("Dosage Form is Unknown.")
            return "Unknown"

    def calculate_datetimes(self, total_volume: int, ml_per_hour: int, start_time: datetime | None = None) -> tuple:
        if start_time is None:
            start_time = datetime.now()
        time_dif_min: int | float = total_volume / ml_per_hour * 60
        stop_time: datetime = start_time + timedelta(minutes=time_dif_min)
        return start_time, stop_time
