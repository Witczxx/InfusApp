from datetime import datetime
from unittest.mock import Mock

from infusapp.models.models import Medi
from infusapp.ui import new_medi_ui


def test_run_success(monkeypatch, new_medi_ui_and_service):
    new_medi_ui, fake_medi_service = new_medi_ui_and_service
    monkeypatch.setattr(new_medi_ui, "get_ingredients", lambda: ["medi_1", "medi_2"])
    monkeypatch.setattr(
        new_medi_ui, "choose_ingredient", lambda ingredients_list: "medi_1"
    )
    monkeypatch.setattr(
        new_medi_ui, "choose_strength", lambda chosen_ingredient: "strength_1"
    )
    fake_medi_service.find_df.return_value = "df_1"
    monkeypatch.setattr(new_medi_ui, "choose_units", lambda: 5)
    monkeypatch.setattr(new_medi_ui, "choose_carrier_fluid", lambda: "NaCl 0.9%")
    monkeypatch.setattr(new_medi_ui, "choose_total_volume", lambda: 1000)
    monkeypatch.setattr(new_medi_ui, "track_infusion", lambda: (70, 250))
    monkeypatch.setattr(
        new_medi_ui.medi_service,
        "calculate_datetimes",
        lambda total_volume, ml_per_hour: (
            datetime(2020, 1, 2, 18, 0),
            datetime(2020, 1, 2, 19, 15),
        ),
    )
    result = new_medi_ui.run()
    assert isinstance(result, Medi)
    assert result.ingredient == "medi_1"
    assert result.strength == "strength_1"
    assert result.unit == 5
    assert result.carrier_fluid == "NaCl 0.9%"
    assert result.total_volume == 1000
    assert result.drops_per_min == 70
    assert result.ml_per_hour == 250
    assert result.start_time == datetime(2020, 1, 2, 18, 0)
    assert result.stop_time == datetime(2020, 1, 2, 19, 15)


def test_get_ingredients(monkeypatch, new_medi_ui_and_service):
    new_medi_ui, fake_medi_service = new_medi_ui_and_service
    answers_1 = iter(
        [None, ["medi_1", "medi_2", "medi_3"], ["medi_1", "medi_2", "medi_3"]]
    )
    answers_2 = iter([None, ["medi_1", "medi_2"]])
    monkeypatch.setattr(
        new_medi_ui.medi_ui_helper,
        "get_ingredients_input_data",
        lambda medi_service: (next(answers_1), "medi_1"),
    )
    monkeypatch.setattr(
        new_medi_ui.medi_ui_helper,
        "get_ingredients_list",
        lambda medi_service, fetched_data, user_input: next(answers_2),
    )
    result = new_medi_ui.get_ingredients()
    assert isinstance(result, list)
    assert result == ["medi_1", "medi_2"]


def test_choose_ingredient_from_list(monkeypatch, new_medi_ui_and_service):
    new_medi_ui, fake_medi_service = new_medi_ui_and_service
    monkeypatch.setattr(
        new_medi_ui.medi_ui_helper,
        "choose_ingredient_input",
        lambda ingredients_list: "medi_1",
    )
    result = new_medi_ui.choose_ingredient(ingredients_list=["medi_1", "medi_2"])
    assert result == "medi_1"


def test_choose_ingredient_from_str(monkeypatch, capsys, new_medi_ui_and_service):
    new_medi_ui, fake_medi_service = new_medi_ui_and_service
    result = new_medi_ui.choose_ingredient(
        ingredients_list=[
            "medi_1",
        ]
    )
    capture = capsys.readouterr()
    assert "Automatically" in capture.out
    assert result == "medi_1"


def test_choose_strength_from_list(monkeypatch, new_medi_ui_and_service):
    new_medi_ui, fake_medi_service = new_medi_ui_and_service
    fake_medi_service.find_strengths.return_value = ["strength_1", "strength_2"]
    monkeypatch.setattr(
        new_medi_ui.medi_ui_helper,
        "choose_strength_input",
        lambda strengths: "strength_1",
    )
    result = new_medi_ui.choose_strength(chosen_ingredient="medi_1")
    assert result == "strength_1"


def test_choose_strength_from_str(monkeypatch, capsys, new_medi_ui_and_service):
    new_medi_ui, fake_medi_service = new_medi_ui_and_service
    fake_medi_service.find_strengths.return_value = ["strength_1"]
    result = new_medi_ui.choose_strength(chosen_ingredient="medi_1")
    capture = capsys.readouterr()
    assert "Automatically" in capture.out
    assert result == "strength_1"


def test_choose_units_choice_1(monkeypatch, new_medi_ui_and_service):
    new_medi_ui, fake_medi_service = new_medi_ui_and_service
    monkeypatch.setattr(
        new_medi_ui.medi_ui_helper, "choose_units_choice_1", lambda units: 0
    )
    result = new_medi_ui.choose_units()
    assert isinstance(result, int)
    assert result == 1


def test_choose_units_choice_2(monkeypatch, new_medi_ui_and_service):
    new_medi_ui, fake_medi_service = new_medi_ui_and_service
    monkeypatch.setattr(
        new_medi_ui.medi_ui_helper, "choose_units_choice_1", lambda units: 3
    )
    monkeypatch.setattr(
        new_medi_ui.medi_ui_helper, "choose_units_choice_2", lambda units, more_units: 2
    )
    result = new_medi_ui.choose_units()
    assert isinstance(result, int | float)
    assert result == 0.25


def test_choose_units_choice_3(monkeypatch, new_medi_ui_and_service):
    new_medi_ui, fake_medi_service = new_medi_ui_and_service
    monkeypatch.setattr(
        new_medi_ui.medi_ui_helper, "choose_units_choice_1", lambda units: 3
    )
    monkeypatch.setattr(
        new_medi_ui.medi_ui_helper, "choose_units_choice_2", lambda units, more_units: 3
    )
    monkeypatch.setattr(new_medi_ui.medi_ui_helper, "choose_units_choice_3", lambda: 8)
    result = new_medi_ui.choose_units()
    assert isinstance(result, int | float)
    assert result == 8


def test_carrier_fluid_is_none(monkeypatch, new_medi_ui_and_service):
    new_medi_ui, fake_medi_service = new_medi_ui_and_service
    monkeypatch.setattr(
        new_medi_ui.medi_ui_helper, "ask_if_carrier_fluid_needed", lambda: False
    )
    result = new_medi_ui.choose_carrier_fluid()
    assert result is None


def test_carrier_fluid_is_other(monkeypatch, new_medi_ui_and_service):
    new_medi_ui, fake_medi_service = new_medi_ui_and_service
    monkeypatch.setattr(
        new_medi_ui.medi_ui_helper, "ask_if_carrier_fluid_needed", lambda: True
    )
    monkeypatch.setattr(
        new_medi_ui.medi_ui_helper,
        "choose_carrier_fluid_input",
        lambda carrier_fluids: 2,
    )
    result = new_medi_ui.choose_carrier_fluid()
    assert result == "Other"


def test_carrier_fluid_is_input(monkeypatch, new_medi_ui_and_service):
    new_medi_ui, fake_medi_service = new_medi_ui_and_service
    monkeypatch.setattr(
        new_medi_ui.medi_ui_helper, "ask_if_carrier_fluid_needed", lambda: True
    )
    monkeypatch.setattr(
        new_medi_ui.medi_ui_helper,
        "choose_carrier_fluid_input",
        lambda carrier_fluids: 3,
    )
    monkeypatch.setattr("builtins.input", lambda prompt: "Sterile Water")
    result = new_medi_ui.choose_carrier_fluid()
    assert result == "Sterile Water"


def test_choose_total_volume_1000(monkeypatch, capsys, new_medi_ui_and_service):
    new_medi_ui, fake_medi_service = new_medi_ui_and_service
    answer = iter([0, 1001, "One Thousand", 1000])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answer))
    result = new_medi_ui.choose_total_volume()
    capture = capsys.readouterr()
    assert "Please choose a number in the given Range (1-1000)." in capture.out
    assert "Input is not a number" in capture.out
    assert result == 1000


def test_track_infusion(monkeypatch, capsys, new_medi_ui_and_service):
    new_medi_ui, fake_medi_service = new_medi_ui_and_service
    answer = iter([None, (25, 250)])
    monkeypatch.setattr(new_medi_ui.infusion_tracker, "menu", lambda: next(answer))
    result = new_medi_ui.track_infusion()
    capture = capsys.readouterr()
    assert "Not enough Data" in capture.out
    assert result == (25, 250)
