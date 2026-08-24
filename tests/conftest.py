import pytest
from infusapp.db.connection import Database
from scripts.schema import create_table_nurses
from infusapp.db.nurse_repository import NurseRepository
from infusapp.services.nurse_service import NurseService
from infusapp.ui.auth_nurse_ui import AuthNurseUi
from unittest.mock import Mock

@pytest.fixture
def db(tmp_path) -> Database:
    db = Database(db_path=tmp_path / "test_db")
    create_table_nurses(db=db)
    return db

@pytest.fixture
def nurse_repository(tmp_path) -> NurseRepository:
    db = Database(db_path=tmp_path / "test_db")
    create_table_nurses(db=db)
    return NurseRepository(db=db)

@pytest.fixture
def nurse_service(tmp_path) -> NurseService:
    db = Database(db_path=tmp_path / "test_db")
    create_table_nurses(db=db)
    nurse_rep = NurseRepository(db=db)
    return NurseService(nurse_rep=nurse_rep)

@pytest.fixture
def auth_nurse_ui_and_service() -> tuple:
    fake_nurse_service = Mock()
    return AuthNurseUi(nurse_service=fake_nurse_service), fake_nurse_service

@pytest.fixture
def anna(nurse_service) -> dict:
    name = "Anna Schmidt"; pw = "test1234"
    nurse = nurse_service.registration(nurse_name=name, pw=pw)
    return {"nurse": nurse, "name": name, "pw": pw}
