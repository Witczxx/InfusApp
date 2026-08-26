from unittest.mock import Mock

import pytest

from infusapp.db.connection import Database
from infusapp.db.nurse_repository import NurseRepository
from infusapp.db.patient_repository import PatientRepository
from infusapp.services.nurse_service import NurseService
from infusapp.services.patient_service import PatientService
from scripts.schema import create_table_nurses, create_table_patients


@pytest.fixture
def db(tmp_path) -> Database:
    db = Database(db_path=tmp_path / "test_db")
    create_table_nurses(db=db)
    create_table_patients(db=db)
    return db


@pytest.fixture
def nurse_repository(db) -> NurseRepository:
    return NurseRepository(db=db)


@pytest.fixture
def nurse_service(nurse_repository) -> NurseService:
    return NurseService(nurse_rep=nurse_repository)


@pytest.fixture
def patient_repository(db) -> PatientRepository:
    return PatientRepository(db=db)


@pytest.fixture
def patient_service(patient_repository) -> PatientService:
    return PatientService(patient_rep=patient_repository)
