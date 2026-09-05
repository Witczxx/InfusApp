import random
import re
from sqlite3 import Row

from infusapp.models.models import Patient


class PatientService:
    def __init__(self, patient_rep):
        self.patient_rep = patient_rep

    def search_for_patient(self, user_input: str) -> Patient | None:
        finding: Row | None = self.patient_rep.search_by_input(user_input=user_input)
        patient: Patient | None = Patient(patient_id=finding["patient_id"], patient_name=finding["patient_name"]) if finding is not None else None
        return patient

    def register_patient(self, user_input: str) -> Patient | None:
        user_input = user_input.strip().title()
        if not self.val_patient_name(user_input=user_input):
            print("\nInvalid Patient Name. Please try again")
            return None
        patient_id = self.generate_patient_id()
        patient = self.patient_rep.add_to_db(patient_id=patient_id, patient_name=user_input)
        patient = Patient(patient_id=patient["patient_id"], patient_name=patient["patient_name"])
        return patient

    def val_patient_name(self, user_input):
        return bool(re.search(r"^[\w]{2,16} [\w]{2,16}$", user_input.strip()))

    def generate_patient_id(self):
        while True:
            id: int = random.randrange(start=1000000000, stop=9999999999)
            id_exists: Row | None = self.patient_rep.search_by_input(user_input=str(id))
            if not id_exists:
                return id
