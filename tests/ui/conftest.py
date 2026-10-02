from unittest.mock import Mock

import pytest

from infusapp.models.models import Nurse
from infusapp.ui.auth_nurse_ui import AuthNurseUi
from infusapp.ui.home_ui import HomeUi
from infusapp.ui.new_infusion_ui import NewInfusionUi
from infusapp.ui.new_medi_ui import NewMediUi
from infusapp.ui.new_patient_ui import NewPatientUi
from infusapp.ui.record_ui import RecordUi


@pytest.fixture
def nurse() -> Nurse:
    return Nurse(nurse_id=1000000, nurse_name="Anna Schmidt")


@pytest.fixture
def auth_nurse_ui_and_service() -> tuple:
    fake_nurse_service = Mock()
    return AuthNurseUi(nurse_service=fake_nurse_service), fake_nurse_service


@pytest.fixture
def new_patient_ui_and__service() -> tuple:
    fake_patient_service = Mock()
    return NewPatientUi(patient_service=fake_patient_service), fake_patient_service


@pytest.fixture
def new_medi_ui_and_service() -> tuple:
    fake_medi_service = Mock()
    return NewMediUi(medi_service=fake_medi_service), fake_medi_service


@pytest.fixture
def new_infusion_ui_and_service(
    nurse, new_patient_ui_and_service, new_medi_ui_and_service
) -> tuple:
    fake_new_patient_ui, _ = new_patient_ui_and_service()
    fake_new_medi_ui, _ = new_medi_ui_and_service()
    fake_infusion_service = Mock()
    return (
        NewInfusionUi(
            infusion_service=fake_infusion_service,
            new_patient_ui=fake_new_patient_ui,
            new_medi_ui=fake_new_medi_ui,
            nurse=nurse,
        ),
        fake_infusion_service,
    )


@pytest.fixture
def new_record_ui_and_service() -> tuple:
    fake_record_service = Mock()
    return RecordUi(record_rep=fake_record_service), fake_record_service


@pytest.fixture
def home_ui(
    nurse, new_infusion_ui_and_service, new_record_ui_and_service
) -> HomeUi:
    fake_new_infusion_ui, _ = new_infusion_ui_and_service()
    fake_record_ui, _ = new_record_ui_and_service()
    return HomeUi(
        nurse=nurse,
        new_infusion_ui=fake_new_infusion_ui,
        record_ui=fake_record_ui,
    )
