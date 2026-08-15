from pathlib import Path

from infusapp.auth_nurse_ui import AuthNurseUi
from infusapp.home_ui import HomeUi
from infusapp.medi_service import MediService
from infusapp.nurse_service import NurseService
from infusapp.patient_service import PatientService
from infusapp.record_ui import RecordUi

db_path = Path(__file__).parent / "medi_database.json"


class Main:
    def __init__(self):
        self.nurse_service = NurseService()
        self.patient_service = PatientService()
        self.medi_service = MediService(filepath=db_path)

    def run(self):

        # Nurse - Login / Registration
        auth_nurse_ui = AuthNurseUi(nurse_service=self.nurse_service)
        nurse_name = auth_nurse_ui.start_screen()

        # Homescreen - Record Infusion / Check Records / Tutorial / Exit
        home_ui = HomeUi(actual_nurse=nurse_name)
        choice = home_ui.show_menu()

        # Record Infusion (1)
        if choice == "Record Infusion":
            record_ui = RecordUi(
                actual_nurse=nurse_name,
                patient_service=self.patient_service,
                medi_service=self.medi_service,
            )
            recorded_data = record_ui.start()


if __name__ == "__main__":
    app = Main()
    app.run()
