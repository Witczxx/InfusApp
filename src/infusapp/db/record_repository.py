class RecordRepository:

    def __init__(self, db):
        self.db = db

    def get_records(self, nurse):
        return self.db.fetch_all(
            ("""
               SELECT patient_name, ingredient, strength, unit, total_volume, ml_per_hour,
               strftime('%Y-%m-%d %H:%M:%S', start_time) AS start_time,
               strftime('%Y-%m-%d %H:%M:%S', stop_time)  AS stop_time
               FROM infusions
               WHERE nurse_name = ? AND nurse_id = ?
               """),
            (nurse.nurse_name, nurse.nurse_id)
        )
