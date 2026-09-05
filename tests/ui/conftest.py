from unittest.mock import Mock

import pytest

from infusapp.models.models import Nurse
from infusapp.ui.auth_nurse_ui import AuthNurseUi
from infusapp.ui.home_ui import HomeUi
from infusapp.ui.new_medi_ui import NewMediUi
from infusapp.ui.new_patient_ui import NewPatientUi


@pytest.fixture
def auth_nurse_ui_and_service() -> tuple:
    fake_nurse_service = Mock()
    return AuthNurseUi(nurse_service=fake_nurse_service), fake_nurse_service


@pytest.fixture
def home_ui_and_new_infusion_ui_and_record_ui() -> tuple:
    nurse = Nurse(nurse_id=1000000, nurse_name="Anna Schmidt")
    fake_new_infusion_ui = Mock()
    fake_record_ui = Mock()
    return (
        HomeUi(
            nurse=nurse, new_infusion_ui=fake_new_infusion_ui, record_ui=fake_record_ui
        ),
        fake_new_infusion_ui,
        fake_record_ui,
    )


@pytest.fixture
def new_patient_ui_and__service() -> tuple:
    fake_patient_service = Mock()
    return NewPatientUi(patient_service=fake_patient_service), fake_patient_service


@pytest.fixture
def new_medi_ui_and_service() -> tuple:
    fake_medi_service = Mock()
    return NewMediUi(medi_service=fake_medi_service), fake_medi_service
