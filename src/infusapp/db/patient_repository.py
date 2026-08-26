from sqlite3 import Row


class PatientRepository:
    def __init__(self, db):
        self.db = db

    def search_by_input(self, user_input: str | int) -> Row | None:
        return self.db.fetchone(
            ("""
                   SELECT patient_id, patient_name FROM patients WHERE patient_id = ? or patient_name = ?
                 """),
            (user_input, user_input),
        )

    def add_to_db(self, patient_name: str, patient_id: int) -> Row:
        self.db.execute(
            ("""
                 INSERT INTO patients (patient_id, patient_name)
                 VALUES (?, ?)
                 """),
            (patient_id, patient_name),
        )
        return self.db.fetchone(
            ("""
                 SELECT patient_id, patient_name FROM patients where patient_id = ?
                 """),
            (patient_id,),
        )
