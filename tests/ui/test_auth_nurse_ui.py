from infusapp.models.models import Nurse

def test_login_success(monkeypatch, auth_nurse_ui_and_service):
    auth_nurse_ui, fake_nurse_service = auth_nurse_ui_and_service
    monkeypatch.setattr("builtins.input", lambda prompt="": "Anna Schmidt")
    monkeypatch.setattr("infusapp.ui.auth_nurse_ui.pwinput", lambda prompt="", mask="*": "test1234")
    nurse = Nurse(nurse_id=1000000, nurse_name="Anna Schmidt")
    fake_nurse_service.login.return_value = nurse
    result = auth_nurse_ui.login_nurse()
    assert result is nurse

def test_login_fail(monkeypatch, auth_nurse_ui_and_service):
    auth_nurse_ui, fake_nurse_service = auth_nurse_ui_and_service
    monkeypatch.setattr("builtins.input", lambda prompt="": "Anna Schmidt")
    monkeypatch.setattr("infusapp.ui.auth_nurse_ui.pwinput", lambda prompt="", mask="*": "test1234")
    fake_nurse_service.login.return_value = None
    result = auth_nurse_ui.login_nurse()
    assert result is None

def test_register_success(monkeypatch, auth_nurse_ui_and_service):
    auth_nurse_ui, fake_nurse_service = auth_nurse_ui_and_service
    monkeypatch.setattr("builtins.input", lambda prompt="": "Anna Schmidt")
    monkeypatch.setattr("infusapp.ui.auth_nurse_ui.pwinput", lambda prompt="", mask="*": "test1234")
    nurse = Nurse(nurse_id=1000000, nurse_name="Anna Schmidt")
    fake_nurse_service.registration.return_value = nurse
    result = auth_nurse_ui.register_nurse()
    assert result is nurse

def test_register_fail_rpw(monkeypatch, auth_nurse_ui_and_service):
    auth_nurse_ui, fake_nurse_service = auth_nurse_ui_and_service
    monkeypatch.setattr("builtins.input", lambda prompt="": "Anna Schmidt")
    passwords = iter(["test1234", "test1235"])
    monkeypatch.setattr("infusapp.ui.auth_nurse_ui.pwinput", lambda prompt="", mask="*": next(passwords))
    nurse = Nurse(nurse_id=1000000, nurse_name="Anna Schmidt")
    fake_nurse_service.registration.return_value = nurse
    result = auth_nurse_ui.register_nurse()
    assert result is None

def test_register_fail_register_nurse(monkeypatch, auth_nurse_ui_and_service, capsys):
    auth_nurse_ui, fake_nurse_service = auth_nurse_ui_and_service
    monkeypatch.setattr("builtins.input", lambda prompt="": "Anna Schmidt")
    monkeypatch.setattr("infusapp.ui.auth_nurse_ui.pwinput", lambda prompt="", mask="*": "test1234")
    fake_nurse_service.registration.return_value = None
    result = auth_nurse_ui.register_nurse()
    assert result is None
    capture = capsys.readouterr()
    assert "Failed" in capture.out

def test_login_or_register_1_success(monkeypatch, auth_nurse_ui_and_service):
    auth_nurse_ui, fake_nurse_service = auth_nurse_ui_and_service
    monkeypatch.setattr("builtins.input", lambda prompt="": "1")
    result = auth_nurse_ui.login_or_register()
    assert result == 1

def test_login_or_register_retries_on_invalid_input(monkeypatch, auth_nurse_ui_and_service):
    auth_nurse_ui, fake_nurse_service = auth_nurse_ui_and_service
    answers = iter(["3", "4", "2"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))
    result = auth_nurse_ui.login_or_register()
    assert result == 2

def test_run_login_success(monkeypatch, auth_nurse_ui_and_service):
    auth_nurse_ui, fake_nurse_service = auth_nurse_ui_and_service
    monkeypatch.setattr(auth_nurse_ui, "login_or_register", lambda: 1)
    nurse = Nurse(nurse_id=1000000, nurse_name="Anna Schmidt")
    monkeypatch.setattr(auth_nurse_ui, "login_nurse", lambda: nurse)
    result = auth_nurse_ui.run()
    assert result is nurse

def test_run_retries_on_invalid_input(monkeypatch, auth_nurse_ui_and_service):
    auth_nurse_ui, fake_nurse_service = auth_nurse_ui_and_service
    answers = iter([3, 4, 2])
    monkeypatch.setattr(auth_nurse_ui, "login_or_register", lambda: next(answers))
    nurse = Nurse(nurse_id=1000000, nurse_name="Anna Schmidt")
    monkeypatch.setattr(auth_nurse_ui, "register_nurse", lambda: nurse)
    result = auth_nurse_ui.run()
    assert result is nurse
