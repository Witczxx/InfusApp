import pytest
import sqlite3


@pytest.fixture
def anna(nurse_service) -> dict:
    name = "Anna Schmidt"
    pw = "test1234"
    nurse = nurse_service.registration(nurse_name=name, pw=pw)
    return {"nurse": nurse, "name": name, "pw": pw}


@pytest.fixture
def max(patient_service) -> dict:
    name = "Max Mustermann"
    patient = patient_service.register_patient(user_input=name)
    return {"patient": patient, "name": patient.patient_name, "id": patient.patient_id}
