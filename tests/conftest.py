from unittest.mock import Mock
from infusapp.ui.medi_ui_helper import MediUiHelper

import pytest

from infusapp.db.connection import Database
from infusapp.db.medi_repository import MediRepository
from infusapp.db.nurse_repository import NurseRepository
from infusapp.db.patient_repository import PatientRepository
from infusapp.services.medi_service import MediService
from infusapp.services.nurse_service import NurseService
from infusapp.services.patient_service import PatientService
from infusapp.services.infusion_service import InfusionService
from scripts.schema import (
    create_table_medications,
    create_table_nurses,
    create_table_patients,
)


@pytest.fixture
def db(tmp_path) -> Database:
    db = Database(db_path=tmp_path / "test_db")
    create_table_nurses(db=db)
    create_table_patients(db=db)
    create_table_medications(db=db)
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


@pytest.fixture
def medi_repository(db) -> MediRepository:
    return MediRepository(db=db)


@pytest.fixture
def medi_service(medi_repository) -> MediService:
    return MediService(medi_rep=medi_repository)

@pytest.fixture
def medi_ui_helper() -> MediUiHelper:
    return MediUiHelper()
