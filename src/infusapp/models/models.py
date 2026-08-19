from dataclasses import dataclass


@dataclass
class Nurse:
    nurse_id: int
    nurse_name: str
    pw: str


@dataclass
class NurseInfo:
    nurse_id: int
    nurse_name: str


@dataclass
class Patient:
    patient_id: int
    patient_name: str


@dataclass
class Infusion:
    medi_id: int
    medi_name: str
