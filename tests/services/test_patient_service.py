from infusapp.models.models import Patient
from unittest.mock import Mock
import pytest

def test_search_for_patient_success(patient_service, max):
    result: Patient | None = patient_service.search_for_patient(user_input=max["name"])
    assert result is not None
    assert result.patient_id == max["id"]
    assert result.patient_name == max["name"]

def test_serach_for_patient_fails(patient_service):
    result: Patient | None = patient_service.search_for_patient(user_input="Maxx Mustermann")
    assert result is None

def test_register_patient_success(patient_service):
    result: Patient | None = patient_service.register_patient(user_input="Jan Jäger")
    assert result is not None
    assert result.patient_name == "Jan Jäger"


def test_register_patient_if_invalid_name(patient_service):
    result: Patient | None = patient_service.register_patient(user_input="Jan J")
    assert result is None

def test_register_strip_title(patient_service):
    result: Patient | None = patient_service.register_patient(user_input=" jan jäger ")
    assert result is not None
    assert result.patient_name == "Jan Jäger"

def test_val_name_limits(patient_service):
    result_1 = patient_service.val_patient_name(user_input="Anna")
    result_2 = patient_service.val_patient_name(user_input="A Test")
    result_3 = patient_service.val_patient_name(user_input="Test B")
    result_4 = patient_service.val_patient_name(user_input="")
    result_5 = patient_service.val_patient_name(user_input="Te st")
    result_6 = patient_service.val_patient_name(user_input="longestnameeverr longestnameeverr")
    result_7 = patient_service.val_patient_name(user_input="  Anna with Blankspaces  ")
    result_8 = patient_service.val_patient_name(user_input=" Anna Blank ")
    assert result_1 is False and result_2 is False and result_3 is False
    assert result_4 is False and result_5 is True and result_6 is True
    assert result_7 is False and result_8 is True

def test_generate_patient_id_success(monkeypatch, patient_service, patient_repository):
    id_test = iter([123456789, 132546879, 987654321, None])
    monkeypatch.setattr(patient_repository, "search_by_input", lambda user_input: next(id_test))
    result = patient_service.generate_patient_id()
    assert type(result) is int 
