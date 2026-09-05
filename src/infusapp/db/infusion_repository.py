from sqlite3 import Row


class InfusionRepository:
    def __init__(self, db):
        self.db = db

    def add_to_db(self, nurse, patient, medi) -> None:
        return self.db.execute(
            ("""
                       INSERT INTO infusions(
                           nurse_id,
                           nurse_name,
                           patient_id,
                           patient_name,
                           ingredient,
                           strength,
                           unit,
                           dosage_form,
                           carrier_fluid,
                           total_volume,
                           drops_per_min,
                           ml_per_hour,
                           start_time,
                           stop_time
                       )
                       VALUES
                           (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   """),
            (
                nurse.nurse_id,
                nurse.nurse_name,
                patient.patient_id,
                patient.patient_name,
                medi.ingredient,
                medi.strength,
                medi.unit,
                medi.dosage_form,
                medi.carrier_fluid,
                medi.total_volume,
                medi.drops_per_min,
                medi.ml_per_hour,
                medi.start_time,
                medi.stop_time,
            ),
        )
