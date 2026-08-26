from unittest.mock import Mock

import pytest

from infusapp.ui.home_ui import HomeUi


def test_choose_one_to_four(monkeypatch, home_ui_and_new_infusion_ui_and_record_ui):
    home_ui, fake_new_infusion_ui, fake_record_ui = (
        home_ui_and_new_infusion_ui_and_record_ui
    )
    answers = iter(["", "5", "0", "1", "2", "3", "4"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))
    result_1 = home_ui.choose_one_to_four()
    result_2 = home_ui.choose_one_to_four()
    result_3 = home_ui.choose_one_to_four()
    result_4 = home_ui.choose_one_to_four()
    assert result_1 == 1
    assert result_2 == 2
    assert result_3 == 3
    assert result_4 == 4


def test_run_1(monkeypatch, home_ui_and_new_infusion_ui_and_record_ui):
    home_ui, fake_new_infusion_ui, fake_record_ui = (
        home_ui_and_new_infusion_ui_and_record_ui
    )
    monkeypatch.setattr(home_ui, "choose_one_to_four", lambda: 1)
    home_ui.run()
    fake_new_infusion_ui.run.assert_called_once()


def test_run_1_fail(monkeypatch, capsys, home_ui_and_new_infusion_ui_and_record_ui):
    home_ui, fake_new_infusion_ui, fake_record_ui = (
        home_ui_and_new_infusion_ui_and_record_ui
    )
    answers = iter([0, 1])
    monkeypatch.setattr(home_ui, "choose_one_to_four", lambda: next(answers))
    home_ui.run()
    capture = capsys.readouterr()
    assert "Input is not" in capture.out


def test_run_2(monkeypatch, home_ui_and_new_infusion_ui_and_record_ui):
    home_ui, fake_new_infusion_ui, fake_record_ui = (
        home_ui_and_new_infusion_ui_and_record_ui
    )
    monkeypatch.setattr(home_ui, "choose_one_to_four", lambda: 2)
    home_ui.run()
    fake_record_ui.run.assert_called_once()


def test_run_3(monkeypatch, home_ui_and_new_infusion_ui_and_record_ui):
    home_ui, fake_new_infusion_ui, fake_record_ui = (
        home_ui_and_new_infusion_ui_and_record_ui
    )
    monkeypatch.setattr(home_ui, "choose_one_to_four", lambda: 3)
    mock_explanation = Mock()
    monkeypatch.setattr(home_ui, "app_explanation", mock_explanation)
    home_ui.run()
    mock_explanation.assert_called_once()


def test_run_4(monkeypatch, home_ui_and_new_infusion_ui_and_record_ui):
    home_ui, fake_new_infusion_ui, fake_record_ui = (
        home_ui_and_new_infusion_ui_and_record_ui
    )
    monkeypatch.setattr(home_ui, "choose_one_to_four", lambda: 4)
    with pytest.raises(SystemExit):
        home_ui.run()

def test_app_explanation(monkeypatch, tmp_path, capsys, home_ui_and_new_infusion_ui_and_record_ui):
    home_ui, _, _ = home_ui_and_new_infusion_ui_and_record_ui
    expl_file = tmp_path / "app_explanation.md"
    expl_file.write_text("Here is an example text.")
    home_ui.expl_path = expl_file
    monkeypatch.setattr("builtins.input", lambda prompt="": "")
    monkeypatch.setattr(home_ui, "run", Mock())
    home_ui.app_explanation()
    capture = capsys.readouterr()
    assert "Here is an example text." in capture.out
    home_ui.run.assert_called_once()
