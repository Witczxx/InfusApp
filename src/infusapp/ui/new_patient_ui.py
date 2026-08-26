from infusapp.models.models import Patient

class NewPatientUi:
    def __init__(self, patient_service):
        self.patient_service = patient_service

    def run(self) -> Patient | None:
        patient, user_input = self.choose_patient()
        if patient is None:
            patient = self.ask_to_register_patient(user_input=user_input)
        if patient is not None:
            print("\n---Patient Chosen---")
            print(f"Name: {patient.patient_name}")
            print(f"ID: {patient.patient_id}")
            return patient
        else:
            self.run()

    def choose_patient(self) -> tuple:
        print("\n---Choose Patient---")
        print("Enter the Patient's Name (First, Last) or ID")
        user_input = input("Input: ")
        patient: Patient | None = self.patient_service.search_for_patient(user_input=user_input)
        return patient, user_input

    def ask_to_register_patient(self, user_input: str) -> Patient | None:
        print("\nThis name is not registered yet.")
        print("Would you like to register the patient with your given input? (y/n)")
        ask_first_infusion = input("Input: ").lower()
        if ask_first_infusion == "y":
            patient: Patient = self.patient_service.register_patient(
                user_input=user_input
            )
            return patient
        elif ask_first_infusion == "n":
            print("\n---Search for the Patient again---")
            self.choose_patient()
        else:
            print("Answer is not 'y' or 'n'. Try again.")
            self.ask_to_register_patient(user_input=user_input)
