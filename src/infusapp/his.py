import random
import re
from dataclasses import dataclass

from model import Nurse, Patient


@dataclass
class NurseInfo:
    nurse_id: str
    nurse_name: str


class His:
    def __init__(self):
        self.nurses = []
        self.nurses.append(Nurse("1000000", "Max Mustermann", "max10"))
        self.patients = []
        self.patients.append(Patient("1000000000", "Anna Schmidt"))

    ### REGISTRATION
    def register_nurse(self, nurse_name, pw):
        # Is the Name valid?
        if not self.val_nurse_name(nurse_name=nurse_name):
            raise ValueError(
                "\n---Invalid Nurse Name---\nEnter your first and last name (e.g. Max Mustermann)"
            )
        # Is the Name taken?
        if self.nurse_name_exists(nurse_name=nurse_name):
            raise ValueError("\n---This name is already taken---")
        # Is the Password valid?
        if not self.val_pw(pw):
            raise ValueError(
                "\n---Invalid Password---\nEnter a password with 8 - 32 characters"
            )
        # Generate a Unique ID
        nurse_id = self.generate_nurse_id()
        # Add User to the Database
        new_nurse = Nurse(nurse_id=nurse_id, nurse_name=nurse_name, pw=pw)
        self.nurses.append(new_nurse)
        return NurseInfo(nurse_id=new_nurse.nurse_id, nurse_name=new_nurse.nurse_name)

    ### LOGIN
    def login_nurse(self, pw, nurse_id=None, nurse_name=None):
        # Does ID exist?
        if nurse_id is not None:
            if not self.nurse_id_exists(nurse_id=nurse_id):
                raise ValueError("\n---Name, ID or Password wrong.---")
            nurse_name = self.get_nurse_name_by_id(nurse_id=nurse_id)
        # Does Name exist?
        elif nurse_name is not None:
            if not self.nurse_name_exists(nurse_name=nurse_name):
                raise ValueError("\n---Name, ID or Password wrong.---")
            nurse_id = self.get_nurse_id_by_name(nurse_name=nurse_name)
        # Is the Password Valid?
        if not self.verify_pw(nurse_id=nurse_id, pw=pw):
            raise ValueError("\n---Name, ID or Password wrong.---")
        return nurse_name

    ### FUNCTIONS FOR NURSE ID
    # Generate ID
    def generate_nurse_id(self):
        while True:
            nurse_id = str(random.randrange(1000000, 9999999))
            for nurse in self.nurses:
                if nurse_id == nurse.nurse_id:
                    break
            else:
                return nurse_id

    # Is ID Valid?
    def val_nurse_id(self, nurse_id):
        if match := re.search(r"^[0-9]{7}$", nurse_id.strip()):
            return True
        else:
            return False

    # Is ID Taken?
    def nurse_id_exists(self, nurse_id):
        for nurse in self.nurses:
            if nurse_id == nurse.nurse_id:
                return True
        return False

    # Find ID with Nurse Name
    def get_nurse_name_by_id(self, nurse_id):
        for nurse in self.nurses:
            if nurse_id == nurse.nurse_id:
                return nurse.nurse_name

    ### FUNCTIONS FOR NURSE NAME
    # Is Name Valid?
    def val_nurse_name(self, nurse_name):
        return bool(re.search(r"^[a-zA-Z]{2,16} [a-zA-Z]{2,16}$", nurse_name.strip()))

    # Is Name Taken?
    def nurse_name_exists(self, nurse_name):
        for nurse in self.nurses:
            if nurse_name == nurse.nurse_name:
                return True

    # Find Name with ID
    def get_nurse_id_by_name(self, nurse_name):
        for nurse in self.nurses:
            if nurse_name == nurse.nurse_name:
                return nurse.nurse_id

    ### FUNCTIONS FOR PASSWORDS
    # Is Password Valid?
    def val_pw(self, pw):
        return bool(re.search(r"^.{8,32}$", pw))

    # Does Password fit to ID/Name ?
    def verify_pw(self, nurse_id, pw):
        for nurse in self.nurses:
            if nurse_id == nurse.nurse_id and pw == nurse.pw:
                return True

    ### FUNCTIONS FOR PATIENT
    # Login
    def login_patient(self, patient_name=None, patient_id=None):
        # Does ID exist?
        if patient_id is not None:
            if not self.patient_id_exists(patient_id=patient_id):
                raise ValueError("\n---Patient ID does not exist---")
            patient_name = self.get_patient_name_by_id(patient_id=patient_id)
        # Does Name exist?
        elif patient_name is not None:
            if not self.patient_name_exists(patient_name=patient_name):
                raise ValueError("\n---Patient not found---")
            patient_id = self.get_patient_id_by_name(patient_name=patient_name)
        return Patient(patient_id=patient_id, patient_name=patient_name)

    # Registration
    def register_patient(self, patient_name):
        # Is the Name valid?
        if not self.val_patient_name(patient_name=patient_name):
            raise ValueError(
                "\n---Invalid Patient Name---\nEnter the first and last name (e.g. Max Mustermann)"
            )
        # Is the Name taken?
        if self.patient_name_exists(patient_name=patient_name):
            raise ValueError("\n---Patient already exists---")
        # Generate a Unique ID
        patient_id = self.generate_patient_id()
        # Add User to the Database
        new_patient = Patient(patient_id=patient_id, patient_name=patient_name)
        self.patients.append(new_patient)
        return new_patient

    # Does Name exist in Database?
    def patient_name_exists(self, patient_name):
        for patient in self.patients:
            if patient_name == patient.patient_name:
                return True
        return False

    # Does ID exist in Database?
    def patient_id_exists(self, patient_id):
        for patient in self.patients:
            if patient_id == patient.patient_id:
                return True
        return False

    # Find Name with ID
    def get_patient_id_by_name(self, patient_name):
        for patient in self.patients:
            if patient_name == patient.patient_name:
                return patient.patient_id

    # Find ID with Name
    def get_patient_name_by_id(self, patient_id):
        for patient in self.patients:
            if patient_id == patient.patient_id:
                return patient.patient_name

    # Is Name Valid?
    def val_patient_name(self, patient_name):
        return bool(re.search(r"^[a-zA-Z]{2,16} [a-zA-Z]{2,16}$", patient_name.strip()))

    # Is ID Valid?
    def val_patient_id(self, patient_id):
        if match := re.search(r"^[0-9]{10}$", patient_id.strip()):
            return True
        else:
            return False

    # Generate ID
    def generate_patient_id(self):
        while True:
            patient_id = str(random.randrange(1000000000, 9999999999))
            for patient in self.patients:
                if patient_id == patient.patient_id:
                    break
            else:
                return patient_id

    ### FUNCTIONS FOR MEDICATION

    # Login
    def medi_login(self): ...

    # Name Valid?
    def val_medi_name(self): ...

    # ID Valid?
    def val_medi_id(self): ...

    # Name Exists?
    def medi_name_exists(self): ...

    # ID Exists?
    def medi_id_exists(self): ...
