import sys
from pathlib import Path

from infusapp.db.connection import Database
from infusapp.db.nurse_repository import NurseRepository
from infusapp.models.models import Nurse, NurseInfo
from infusapp.services.nurse_service import NurseService
from infusapp.ui.auth_nurse_ui import AuthNurseUi

db_path = Path(__file__).parent.parent / "data" / "infusapp.db"

class Main:
    def __init__(self):
        self.db = Database(db_path=db_path)
        self.nurse_rep = NurseRepository(db=self.db)
        self.nurse_service = NurseService(nurse_rep=self.nurse_rep)
        self.auth_nurse_ui = AuthNurseUi(nurse_service=self.nurse_service)

    # APP STARTPOINT - Nurse - Login / Registration
    def run_login(self) -> None:
        nurse_info: NurseInfo = self.auth_nurse_ui.run()
        return self.run_home(nurse_info = nurse_info)

    ### HOME UI - NEW RECORD / HISTORY / TUTORIAL / EXIT
    def run_home(self, nurse_info: NurseInfo) -> None:
        ...


# -------------------------------------------------

'''
from infusapp import drip_rate_tapper
from infusapp.auth_nurse_ui import AuthNurseUi
from infusapp.home_ui import HomeUi
from infusapp.medi_db import MediDb
from infusapp.medi_service import MediService
from infusapp.nurse_service import NurseService
from infusapp.patient_service import PatientService
from infusapp.record_ui import RecordUi
from infusapp.drip_rate_tapper import DripRateTapper
from infusapp.check_records import CheckRecords

db_path = Path(__file__).parent / "medi_database.txt"
'''

# --------------------------------------------------------

'''
        # Start Database
        self.medi_db = MediDb(filepath=db_path, database="medi.db")
        self.medi_db.create_database()

        self.nurse_service = NurseService()
        self.patient_service = PatientService()
        self.medi_service = MediService(medi_db=self.medi_db)
        self.drip_rate_tapper = DripRateTapper()

        self.actual_nurse = []

        self.infusion_recordings = []
        self.check_records = CheckRecords(self.infusion_recordings)
'''

# -------------------------------------------------

'''
        actual_nurse = auth_nurse_ui.start_screen()
        self.actual_nurse.extend(actual_nurse)
        print(f"\n\n\n---Welcome, {self.actual_nurse[1]}---")
        self.run_home_menu()
'''

# --------------------------------------------------

    def run_home_menu(self):
        try:
            while True:
                # Homescreen - Record Infusion / Check Records / Tutorial / Exit
                home_ui = HomeUi(actual_nurse=self.actual_nurse)
                choice = home_ui.show_menu()

                # Record Infusion (1)
                if choice == "Record Infusion":
                    # Record new Infusion
                    record_ui = RecordUi(
                        actual_nurse=self.actual_nurse,
                        patient_service=self.patient_service,
                        medi_service=self.medi_service,
                        drip_rate_tapper=self.drip_rate_tapper,
                    )
                    infusion_recording = record_ui.record_ui_menu()
                    sorted_recording = record_ui.record_data(infusion_recording=infusion_recording)
                    self.infusion_recordings.append(sorted_recording)
                    print("\n---Data Successfully Documented---")

                # Check Records (3)
                if choice == "Check Records":
                    self.check_records.show_records()


                # Logout and Exit (4)
                elif choice == "Logout and Exit":
                    sys.exit("\n\n---Goodbye! Looking forward to see you soon!---")
        finally:
            # Stop Database
            self.medi_db.close_database()


if __name__ == "__main__":
    Main().run_app()
