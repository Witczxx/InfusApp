from unittest.mock import Mock

from infusapp.models.models import Patient


def test_run_success(monkeypatch, capsys, new_patient_ui_and_service):
    new_patient_ui, fake_patient_service = new_patient_ui_and_service
    monkeypatch.setattr("builtins.input", lambda prompt: "Max Mustermann")
    fake_patient_service.search_for_patient.return_value = Patient(
        patient_name="Max Mustermann", patient_id=1234567890
    )
    result: Patient = new_patient_ui.run()
    capture = capsys.readouterr()
    assert "Patient Chosen" in capture.out
    assert result.patient_name == "Max Mustermann"
    assert result.patient_id == 1234567890


def test_run_choose_patient_is_None(monkeypatch, capsys, new_patient_ui_and_service):
    new_patient_ui, fake_patient_service = new_patient_ui_and_service
    answers = iter(["Max Mustermann", "y"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))
    fake_patient_service.search_for_patient.return_value = None
    fake_patient_service.register_patient.return_value = Patient(
        patient_name="Max Mustermann", patient_id=1234567890
    )
    result: Patient = new_patient_ui.run()
    capture = capsys.readouterr()
    assert "not registered" in capture.out
    assert result.patient_name == "Max Mustermann"
    assert result.patient_id == 1234567890


def test_run_loop(monkeypatch, new_patient_ui_and_service):
    new_patient_ui, fake_patient_service = new_patient_ui_and_service
    answers_1 = iter(["Max Mustermann", "y", "Max Mustermann", "y"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers_1))
    fake_patient_service.search_for_patient.return_value = None
    fake_patient_service.register_patient.side_effect = [
        None,
        Patient(patient_name="Max Mustermann", patient_id=1234567890),
    ]
    spy = Mock(wraps=new_patient_ui.run)
    new_patient_ui.run = spy  # Needed when the program calls it to repeat the prompt
    result: Patient = spy()
    assert spy.call_count == 2
    assert result.patient_name == "Max Mustermann"
    assert result.patient_id == 1234567890

def test_ask_to_register_success(monkeypatch, new_patient_ui_and_service):
    new_patient_ui, fake_patient_service = new_patient_ui_and_service
    monkeypatch.setattr("builtins.input", lambda prompt: "y")
    fake_patient_service.register_patient.return_value = Patient(patient_name="Max Mustermann", patient_id=1234567890)
    result = new_patient_ui.ask_to_register_patient(user_input="Max Mustermann")
    assert result.patient_name == "Max Mustermann"
    assert result.patient_id == 1234567890

def test_ask_to_register_no(monkeypatch, new_patient_ui_and_service):
    new_patient_ui, fake_patient_service = new_patient_ui_and_service
    monkeypatch.setattr("builtins.input", lambda prompt: "n")
    monkeypatch.setattr(new_patient_ui, "run", lambda: True)
    result = new_patient_ui.ask_to_register_patient(user_input="Max Mustermann")
    assert result is True

def test_ask_to_register_fail(monkeypatch, new_patient_ui_and_service):
    new_patient_ui, fake_patient_service = new_patient_ui_and_service
    answers = iter(["x", "y"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))
    fake_patient_service.register_patient.return_value = Patient(patient_name="Max Mustermann", patient_id=1234567890)
    result = new_patient_ui.ask_to_register_patient(user_input="Max Mustermann")
    assert result.patient_name == "Max Mustermann"
    assert result.patient_id == 1234567890
