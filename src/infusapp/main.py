from pathlib import Path

from infusapp.db.connection import Database
from infusapp.db.medi_repository import MediRepository
from infusapp.db.nurse_repository import NurseRepository
from infusapp.db.patient_repository import PatientRepository
from infusapp.db.record_repository import RecordRepository
from infusapp.models.models import Nurse, Patient
from infusapp.services.medi_service import MediService
from infusapp.services.nurse_service import NurseService
from infusapp.services.patient_service import PatientService
from infusapp.ui import new_medi_ui, new_patient_ui
from infusapp.ui.auth_nurse_ui import AuthNurseUi
from infusapp.ui.home_ui import HomeUi
from infusapp.ui.new_infusion_ui import NewInfusionUi
from infusapp.ui.new_medi_ui import NewMediUi
from infusapp.ui.new_patient_ui import NewPatientUi
from infusapp.ui.record_ui import RecordUi
from infusapp.services.infusion_service import InfusionService
from infusapp.db.infusion_repository import InfusionRepository

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

        self.medi_rep = MediRepository(db=self.db)
        self.medi_service = MediService(medi_rep=self.medi_rep)
        self.new_medi_ui = NewMediUi(medi_service=self.medi_service)

        self.infusion_rep = InfusionRepository(db=self.db)
        self.infusion_service = InfusionService(infusion_rep=self.infusion_rep)

        self.record_rep = RecordRepository(db=self.db)
        self.record_ui = RecordUi(record_rep=self.record_rep)

    def run(self) -> None:
        nurse: Nurse = self.auth_nurse_ui.run()
        new_infusion_ui: NewInfusionUi = NewInfusionUi(
            nurse=nurse, new_patient_ui=self.new_patient_ui, new_medi_ui=self.new_medi_ui,
            infusion_service=self.infusion_service
        )
        home_ui = HomeUi(
            nurse=nurse, new_infusion_ui=new_infusion_ui, record_ui=self.record_ui,
        )
        home_ui.run()


if __name__ == "__main__":
    Main().run()
