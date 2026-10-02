import pytest

from infusapp.exceptions.exceptions import DocumentationAborted


def test_get_ingredients_input_data(monkeypatch, medi_ui_helper, medi_service, db):
    db.execute("""
           INSERT INTO medications (ingredient, df, strength, route, trade_name)
           VALUES
           ('MEDI_1', 'DF_1', 'STRENGTH_1', 'ROUTE_1', 'TRADE_NAME_1'),
           ('MEDI_2', 'DF_2', 'STRENGTH_2', 'ROUTE_2', 'TRADE_NAME_2'),
           ('MEDI_3', 'DF_3', 'STRENGTH_3', 'ROUTE_3', 'TRADE_NAME_3'),
           ('DRUG_4', 'DF_4', 'STRENGTH_4', 'ROUTE_4', 'TRADE_NAME_4'),
           ('DRUG_5', 'DF_5', 'STRENGTH_5', 'ROUTE_5', 'TRADE_NAME_5'),
           ('MEDI_1', 'DF_6', 'STRENGTH_6', 'ROUTE_6', 'TRADE_NAME_6')
           """)
    user_input = "medi_1"
    monkeypatch.setattr("builtins.input", lambda prompt: user_input)
    result = medi_ui_helper.get_ingredients_input_data(medi_service=medi_service)
    fetched_data = [
        [row["ingredient"], row["df"], row["strength"], row["route"], row["trade_name"]]
        for row in result[0]
    ]
    assert user_input.upper() == result[1]
    assert fetched_data == [
        ["MEDI_1", "DF_1", "STRENGTH_1", "ROUTE_1", "TRADE_NAME_1"],
        ["MEDI_1", "DF_6", "STRENGTH_6", "ROUTE_6", "TRADE_NAME_6"],
    ]

def test_get_ingredients_quit(monkeypatch, medi_ui_helper, medi_service, db):
    user_input = "q"
    monkeypatch.setattr("builtins.input", lambda prompt: user_input)
    with pytest.raises(DocumentationAborted):
        result = medi_ui_helper.get_ingredients_input_data(medi_service=medi_service)

def test_choose_ingredient_input(monkeypatch, capsys, medi_ui_helper):
    ingredients_list = ["medi_1", "medi_2", "medi_3"]
    answer = iter(["0", "4", "str", "1"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answer))
    result = medi_ui_helper.choose_ingredient_input(ingredients_list=ingredients_list)
    capture = capsys.readouterr()
    assert result == ingredients_list[0]
    assert "Please choose a number in the given range" in capture.out
    assert "Input is not a number" in capture.out

def test_choose_ingredient_input_quit(monkeypatch, medi_ui_helper):
    ingredients_list = ["medi_1", "medi_2", "medi_3"]
    monkeypatch.setattr("builtins.input", lambda prompt: "Q")
    with pytest.raises(DocumentationAborted):
        result = medi_ui_helper.choose_ingredient_input(ingredients_list=ingredients_list)

def test_choose_strength_input(monkeypatch, capsys, medi_ui_helper):
    strengths = ["strength_1", "strength_2", "strength_3"]
    answers = iter(["0", "4", "abc", "2"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))
    result = medi_ui_helper.choose_strength_input(strengths=strengths)
    capture = capsys.readouterr()
    assert result == strengths[1]
    assert "Please choose a number in the given range" in capture.out
    assert "Input is not a number" in capture.out

def test_choose_strength_input_quit(monkeypatch, medi_ui_helper):
    strengths = ["strength_1", "strength_2", "strength_3"]
    monkeypatch.setattr("builtins.input", lambda prompt: "Q")
    with pytest.raises(DocumentationAborted):
        result = medi_ui_helper.choose_strength_input(strengths=strengths)

def test_choose_units_choice_1(monkeypatch, capsys, medi_ui_helper):
    units = ["1 Unit", "2 Units", "5 Units", "More..."]
    answers = iter(["0", "5", "abc", "2"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))
    result = medi_ui_helper.choose_units_choice_1(units=units)
    capture = capsys.readouterr()
    assert result == 1
    assert "Please" in capture.out

def test_choose_units_choice_2(monkeypatch, capsys, medi_ui_helper):
    units = ["1 Unit", "2 Units", "5 Units", "More..."]
    more_units = ["100%", "50%", "25%", "Enter.."]
    answers = iter(["0", "5", "abc", "2"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))
    result = medi_ui_helper.choose_units_choice_2(units=units, more_units=more_units)
    capture = capsys.readouterr()
    assert result == 1
    assert "Please" in capture.out

def test_choose_units_choice_3(monkeypatch, capsys, medi_ui_helper):
    answers = iter(["0", "10000000", "no_int", "4"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))
    result = medi_ui_helper.choose_units_choice_3()
    capture = capsys.readouterr()
    assert result == 4
    assert "uncommon" in capture.out
    assert "not a number" in capture.out

def test_ask_if_carrier_fluid_needed_yes(monkeypatch, capsys, medi_ui_helper):
    answers = iter(["", "a", "y"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))
    result = medi_ui_helper.ask_if_carrier_fluid_needed()
    capture = capsys.readouterr()
    assert result is True
    assert "recognized" in capture.out

def test_ask_if_carrier_fluid_needed_no(monkeypatch, medi_ui_helper):
    monkeypatch.setattr("builtins.input", lambda prompt: "n")
    result = medi_ui_helper.ask_if_carrier_fluid_needed()
    assert result is False

def test_choose_carrier_fluid_input(monkeypatch, capsys, medi_ui_helper):
    carrier_fluids: list = ["NaCl 0.9%", "Glucose 5%", "Other", "Enter Name"]
    answers = iter(["", "0", "5", "str", "3"])
    monkeypatch.setattr("builtins.input", lambda mock: next(answers))
    result = medi_ui_helper.choose_carrier_fluid_input(carrier_fluids=carrier_fluids)
    assert result == 2

def test_choose_carrier_fluid_input_fail(monkeypatch, capsys, medi_ui_helper):
    carrier_fluids: list = ["NaCl 0.9%", "Glucose 5%", "Other", "Enter Name"]
    monkeypatch.setattr("builtins.input", lambda mock: "q")
    with pytest.raises(DocumentationAborted):
        result = medi_ui_helper.choose_carrier_fluid_input(carrier_fluids=carrier_fluids)
