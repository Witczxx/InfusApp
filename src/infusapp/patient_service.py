import random
import re

from infusapp.model import Patient
from infusapp.service_helper import check_existence, find_by_value, val_name, generate_id


class PatientService:
    def __init__(self):
        self.patients = []
        self.patients.append(
            Patient(patient_id="1000000000", patient_name="Anna Schmidt")
        )

    ### LOGIN
    def login_patient(self, patient_name=None, patient_id=None):
        # ID exists?
        if patient_id is not None:
            if not self.patient_id_exists(patient_id=patient_id):
                raise ValueError("\n---Patient not found---")
            patient_name = self.get_patient_name_by_id(patient_id=patient_id)
        # Name exists?
        elif patient_name is not None:
            if not self.patient_name_exists(patient_name=patient_name):
                raise ValueError("\n---Patient not found---")
            patient_id = self.get_patient_id_by_name(patient_name=patient_name)
        # ID & Name is None
        else:
            raise ValueError("\n---Patient not Found---")
        # Login Successful
        logged_patient = Patient(patient_id=patient_id, patient_name=patient_name)
        return patient_id, patient_name

    # REGISTRATION
    def register_patient(self, patient_name):
        # Name Valid?
        if not self.val_patient_name(patient_name=patient_name):
            raise ValueError(
                "\n---Invalid Patient Name---\nEnter the first and last name (e.g. Max Mustermann)"
            )
        # Name Taken?
        if self.patient_name_exists(patient_name=patient_name):
            raise ValueError("\n---Patient already exists---")
        # Generate ID
        patient_id = self.generate_patient_id()
        # Add to Database
        new_patient = Patient(patient_id=patient_id, patient_name=patient_name)
        self.patients.append(new_patient)
        return patient_id, patient_name

    ### FUNCTIONS

    ### ID VALID?
    def val_patient_id(self, patient_id):
        return bool(re.search(r"^[0-9]{10}$", patient_id.strip()))

    ### NAME VALID?
    def val_patient_name(self, patient_name):
        return bool(re.search(r"^[a-zA-Z]{2,16} [a-zA-Z]{2,16}$", patient_name.strip()))

    ### ID EXISTS?
    def patient_id_exists(self, patient_id):
        return check_existence(
            entries=self.patients, field_name="patient_id", search_value=patient_id
        )

    ### NAME EXISTS?
    def patient_name_exists(self, patient_name):
        return check_existence(
            entries=self.patients, field_name="patient_name", search_value=patient_name
        )

    ### FIND ID
    def get_patient_name_by_id(self, patient_id):
        patient = find_by_value(
            entries=self.patients, field_name="patient_id", search_value=patient_id
        )
        return patient.patient_name if patient is not None else None

    ### FIND NAME
    def get_patient_id_by_name(self, patient_name):
        patient = find_by_value(
            entries=self.patients, field_name="patient_name", search_value=patient_name
        )
        return patient.patient_id if patient is not None else None

    ### GENERATE ID
    def generate_patient_id(self):
        return generate_id(self.patients, "patient_id", 1000000000, 9999999999)
