class RecordRepository:

    def __init__(self, db):
        self.db = db

    def get_records(self, nurse):
        records = self.db.fetch_all(
            ("""
               SELECT (patient_name, ingredient, strength, unit, total_volume, ml_per_hour, start_time, stop_time)
               FROM infusions
               WHERE nurse_name = ? AND nurse_id = ?
               """),
            (nurse.nurse_name, nurse.nurse_id)
        )
