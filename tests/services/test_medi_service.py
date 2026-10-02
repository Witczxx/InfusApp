from datetime import datetime
from types import SimpleNamespace
from unittest.mock import Mock

from infusapp.models.models import Patient


def test_filter_ingredients_by_route(medi_service, db):
    user_input = "medi"
    db.execute("""
               INSERT INTO medications (ingredient, route) 
               VALUES 
               ('medi_3', 'INTRAVENOUS'),
               ('medi_2', 'INJECTION'),
               ('medi_4', 'ORAL'),
               ('medi_2', 'INJECTION'),
               ('medi_1', 'INTRAVENOUS')
               """)
    fetched_data = medi_service.fetch_data(user_input="medi")
    result = medi_service.filter_ingredients_by_route(
        user_input=user_input, fetched_data=fetched_data
    )
    assert len(result) == 3
    assert result == ["medi_1", "medi_2", "medi_3"]


def test_filter_ingredients_by_route_is_none(medi_service, db):
    user_input = "medi"
    db.execute("""
               INSERT INTO medications (ingredient, route) 
               VALUES 
               ('drug_1', 'INTRAVENOUS'),
               ('drug_2', 'INJECTION'),
               ('drug_4', 'ORAL'),
               ('drug_2', 'INJECTION'),
               ('drug_3', 'INTRAVENOUS')
               """)
    fetched_data = medi_service.fetch_data(user_input="medi")
    result = medi_service.filter_ingredients_by_route(
        user_input=user_input, fetched_data=fetched_data
    )
    assert result is None


def test_find_strengths(medi_service, db):
    chosen_ingredient = "drug_1"
    db.execute("""
               INSERT INTO medications (ingredient, strength) 
               VALUES 
               ('drug_1', '10ml/100ml'),
               ('drug_1', '25ml/2000ml'),
               ('drug_1', '30ml/200ml'),
               ('drug_1', '5 Units'),
               ('drug_1', '10ml/100ml'),
               ('drug_2', '3 Units')
               """)
    result = medi_service.find_strengths(chosen_ingredient=chosen_ingredient)
    assert len(result) == 4
    assert result == ["5 Units", "10ml/100ml", "25ml/2000ml", "30ml/200ml"]


def test_find_df(medi_service, db):
    chosen_ingredient = "medi_1"
    strength = "10mL/100mL"
    db.execute("""
               INSERT INTO medications (ingredient, strength, df)
               VALUES
               ('medi_1', '10mL/100mL', 'FOR SOLUTION'),
               ('medi_1', '10mL/100mL', 'INJECTABLE'),
               ('medi_2', '10mL/100mL', 'SOLUTION'),
               ('medi_1', '100mL/100mL', 'SOLUTION'),
               ('medi_1', '10mL/100mL', 'FOR SOLUTION'),
               ('medi_1', '10mL/100mL', 'SOLUTION')
               """)
    result = medi_service.find_df(
        chosen_ingredient=chosen_ingredient, strength=strength
    )
    assert isinstance(result, str)
    assert result == "FOR SOLUTION | INJECTABLE | SOLUTION"


def test_find_df_is_None(medi_service, db):
    chosen_ingredient = "medi_1"
    strength = "10mL/100mL"
    result = medi_service.find_df(
        chosen_ingredient=chosen_ingredient, strength=strength
    )
    assert result == "Unknown"


def test_calculate_datetimes(medi_service):
    total_volume = 500
    ml_per_hour = 250
    start_time = datetime(year=2026, month=12, day=30, hour=10, minute=15)
    result = medi_service.calculate_datetimes(
        total_volume=total_volume, ml_per_hour=ml_per_hour, start_time=start_time
    )
    assert result == (
        datetime(year=2026, month=12, day=30, hour=10, minute=15),
        datetime(year=2026, month=12, day=30, hour=12, minute=15),
    )
