from pathlib import Path

from infusapp.db.connection import Database
from infusapp.db.nurse_repository import NurseRepository
from infusapp.models.models import Nurse
from infusapp.services.nurse_service import NurseService
from infusapp.ui.auth_nurse_ui import AuthNurseUi

db_path = Path(__file__).parent.parent.parent / "data" / "infusapp.db"

class Main:
    def __init__(self, db_path: Path = db_path):
        self.db = Database(db_path=db_path)
        self.nurse_rep = NurseRepository(db=self.db)
        self.nurse_service = NurseService(nurse_rep=self.nurse_rep)
        self.auth_nurse_ui = AuthNurseUi(nurse_service=self.nurse_service)

    def run_login(self) -> None:
        nurse_info: Nurse = self.auth_nurse_ui.run()
        print("We did it!")
        #return self.run_home(nurse_info = nurse_info)
"""
    ### HOME UI - NEW RECORD / HISTORY / TUTORIAL / EXIT
    def run_home(self, nurse_info: Nurse) -> None:
        ...
"""
if __name__ == "__main__":
    Main().run_login()
