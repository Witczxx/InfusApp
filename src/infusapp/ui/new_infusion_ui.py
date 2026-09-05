from infusapp.models.models import Medi, Patient
from sqlite3 import Row


class NewInfusionUi:

    def __init__(self, infusion_service, new_patient_ui, new_medi_ui, nurse):
        self.infusion_service = infusion_service
        self.new_patient_ui = new_patient_ui
        self.new_medi_ui = new_medi_ui
        self.nurse = nurse

    def run(self) -> None:
        print("\n---Record a new Infusion---")
        patient: Patient = self.new_patient_ui.run()
        medi: Medi = self.new_medi_ui.run()
        self.infusion_service.add_to_db(
            nurse=self.nurse, patient=patient, medi=medi
        )
