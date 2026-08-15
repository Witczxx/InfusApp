class RecordUi:

    def __init__(self, actual_nurse, patient_service, medi_service):
        self.actual_nurse = actual_nurse
        self.patient_service = patient_service
        self.medi_service = medi_service
        self.actual_patient = None

    def start(self):
        print("\n\n\n---Record a new Infusion---")
        return self.get_patient()

    ### ASK USER FOR PATIENT
    def get_patient(self):
        # Define Variables
        patient_id = None
        patient_name = None
        # Enter Name or ID
        print("Enter the Patient's Name (First, Last) or ID")
        user_input = input("Input: ")

        # Name was entered
        if self.patient_service.val_patient_name(patient_name=user_input.title()):
            patient_name = user_input.title()
            try:
                patient_id = self.patient_service.get_patient_id_by_name(
                    patient_name=user_input
                )
                actual_patient = self.patient_service.login_patient(
                    patient_id=patient_id, patient_name=patient_name
                )
                # Login Successful!
                print("---Patient Found---")
                return self.confirm_patient_login(actual_patient=actual_patient)
            except ValueError as errormessage:
                print(errormessage)
                return self.ask_to_register_patient(patient_name=patient_name)
        # ID was entererd
        elif self.patient_service.val_patient_id(patient_id=user_input):
            patient_id = user_input
            try:
                patient_name = self.patient_service.get_patient_name_by_id(
                    patient_id=user_input
                )
                actual_patient = self.patient_service.login_patient(
                    patient_id=patient_id, patient_name=patient_name
                )
                # Login Successful!
                print("---Patient Found---")
                return self.confirm_patient_login(actual_patient=actual_patient)
            except ValueError as errormessage:
                print(errormessage)
                return self.get_patient()
        # When neither ID or Name recognized
        else:
            print("Name or ID entered wrong")
            return self.get_patient()

    # When Patient (user_input) was not found:
    def ask_to_register_patient(self, patient_name):
        print("\nIs this the patient's first Infusion? (y/n)")
        ask_first_infusion = input("Input: ").lower()
        # First Infusion -> Registererd
        if ask_first_infusion == "y":
            new_patient = self.patient_service.register_patient(
                patient_name=patient_name
            )
            self.actual_patient = new_patient
            print("\n---Registration Successful!---")
            print(
                f"Patient {self.actual_patient.patient_name.split(' ')[1]}'s new ID is: {self.actual_patient.patient_id}"
            )
            return self.get_medication_name()
        # Not First Infusion -> Repeat
        elif ask_first_infusion == "n":
            print("\n---Search for the Patient again---")
            return self.get_patient()
        # If not entered y/n
        else:
            print("Answer is not 'y' or 'n'. Try again.")
            return self.ask_to_register_patient(patient_name=patient_name)

    # When Patient (user_input) was found:
    def confirm_patient_login(self, actual_patient):
        self.actual_patient = actual_patient
        print(f"Name: {self.actual_patient.patient_name}")
        print(f"ID: {self.actual_patient.patient_id}")
        return self.get_medication_name()

    ### ASK USER FOR MEDICATION
    def get_medication_name(self):
        print("\nPlease enter the Medication's or Liquid's Name")
        medi_name = input("Input: ")
