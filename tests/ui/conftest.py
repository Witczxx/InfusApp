from unittest.mock import Mock

import pytest

from infusapp.models.models import Nurse
from infusapp.ui.auth_nurse_ui import AuthNurseUi
from infusapp.ui.home_ui import HomeUi


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
