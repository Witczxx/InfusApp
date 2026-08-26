from pathlib import Path

from infusapp.db.connection import Database
from infusapp.db.nurse_repository import NurseRepository
from infusapp.db.patient_repository import PatientRepository
from infusapp.db.record_repository import RecordRepository
from infusapp.models.models import Nurse, Patient
from infusapp.services.nurse_service import NurseService
from infusapp.services.patient_service import PatientService
from infusapp.ui.auth_nurse_ui import AuthNurseUi
from infusapp.ui.home_ui import HomeUi
from infusapp.ui.new_infusion_ui import NewInfusionUi
from infusapp.ui.new_patient_ui import NewPatientUi
from infusapp.ui.record_ui import RecordUi

db_path = Path(__file__).parent.parent.parent / "data" / "infusapp.db"


class Main:
    def __init__(self, db_path: Path = db_path):
        self.db = Database(db_path=db_path)

        self.nurse_rep = NurseRepository(db=self.db)
        self.nurse_service = NurseService(nurse_rep=self.nurse_rep)
        self.auth_nurse_ui = AuthNurseUi(nurse_service=self.nurse_service)

        self.patient_rep = PatientRepository(db=self.db)
        self.patient_service = PatientService(patient_rep=self.patient_rep)
        self.new_patient_ui = NewPatientUi(patient_service=self.patient_service)
        self.new_infusion_ui = NewInfusionUi(new_patient_ui=self.new_patient_ui)

        self.record_rep = RecordRepository(db=self.db)
        self.record_ui = RecordUi(record_rep=self.record_rep)

    def run(self) -> None:
        nurse: Nurse = self.auth_nurse_ui.run()
        home_ui = HomeUi(
            nurse=nurse, new_infusion_ui=self.new_infusion_ui, record_ui=self.record_ui
        )
        home_ui.run()


if __name__ == "__main__":
    Main().run()
