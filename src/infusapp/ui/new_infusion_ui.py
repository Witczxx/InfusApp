from infusapp.models.models import Patient

class NewInfusionUi:
    def __init__(self, new_patient_ui):
        self.new_patient_ui = new_patient_ui

    def run(self):
        print("\n---Record a new Infusion---")
        patient: Patient = self.new_patient_ui.run()
