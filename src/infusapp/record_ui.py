from infusapp import drip_rate_tapper


class RecordUi:

    def __init__(self, actual_nurse, patient_service, medi_service, drip_rate_tapper):
        # Assisting Functions
        self.patient_service = patient_service
        self.medi_service = medi_service
        self.drip_rate_tapper = drip_rate_tapper
        # Nurse / Patient / Medication
        self.actual_nurse = actual_nurse
        self.actual_patient = []
        self.actual_medi = []       # Later: [ingredient, strength, found_df]


    def record_ui_menu(self):
        print("\n---Record a new Infusion---")
        # Choose Patient
        print("\n---Choose Patient---")
        actual_patient = self.choose_patient()
        print("\n---Patient Chosen---")
        print(f"Name: {self.actual_patient[1]}")
        print(f"ID: {self.actual_patient[0]}")
        # Choose Medication
        print("\n---Choose Medication---")
        self.actual_medi = self.choose_medi()
        # Choose Units
        print("\n---Choose Units---")
        unit = self.choose_units()
        print(f"\nChosen Unit: {unit}")
        # Choose Carrier Fluid
        print("\n---Choose Carrier Fluid---")
        print("\nIs a Carrier Fluid being added? (y/n)")
        ask_carrier_fluid = input("Input: ")
        while True:
            if ask_carrier_fluid == "y":
                carrier_fluid = self.choose_carrier_fluid()
                print("---Selection Completed---")
                break
            elif ask_carrier_fluid == "n":
                carrier_fluid = None
                print("---Selection Completed---")
                break
            else:
                print("Input not Recognized")
        fluid_volume = self.choose_carrier_volume()
        # Hit the Keyboard
        drops_per_min, ml_per_hour = self.drip_rate_tapper.menu()
        return [self.actual_nurse[0], self.actual_nurse[1], self.actual_patient[0], self.actual_patient[1], self.actual_medi[0], self.actual_medi[1], self.actual_medi[2], unit, carrier_fluid, fluid_volume, drops_per_min, ml_per_hour]

        
    
    ### CHOOSE PATIENT
    def choose_patient(self):
        # Enter Name or ID
        print("Enter the Patient's Name (First, Last) or ID")
        user_input = input("Input: ")
        # ID entered
        patient_id = (
            user_input
            if self.patient_service.val_patient_id(patient_id=user_input)
            else None
        )
        # Name entered
        patient_name = (
            user_input
            if self.patient_service.val_patient_name(patient_name=user_input)
            else None
        )
        # ID & Name is None
        if patient_id is None and patient_name is None:
            print("\n---Input has no valid Format---")
            return self.choose_patient()
        # Try Login
        try:
            actual_patient = self.patient_service.login_patient(
                patient_id=patient_id, patient_name=patient_name
            )
        except ValueError as errormessage:
            print(errormessage)
            return self.ask_to_register_patient(patient_name=patient_name)
        # Login Successful!
        self.actual_patient = actual_patient
        return actual_patient[0], actual_patient[1]

    ### REGISTER PATIENT
    def ask_to_register_patient(self, patient_name):
        # First Infusion? (y/n)
        print("\nIs this the patient's first Infusion? (y/n)")
        ask_first_infusion = input("Input: ").lower()
        # First Infusion (y) -> Registererd
        if ask_first_infusion == "y":
            new_patient = self.patient_service.register_patient(
                patient_name=patient_name
            )
            self.actual_patient = new_patient
            print("\n---Registration Successful!---")
            print(
                f"Patient {self.actual_patient[1].split(' ')[1]}'s new ID is: {self.actual_patient[0]}"
            )
            return self.actual_patient[0], self.actual_patient[1]
        # Not First Infusion (n) -> Repeat
        elif ask_first_infusion == "n":
            print("\n---Search for the Patient again---")
            return self.choose_patient()
        # If not entered y/n
        else:
            print("Answer is not 'y' or 'n'. Try again.")
            return self.ask_to_register_patient(patient_name=patient_name)

    ### CHOOSE MEDICATION
    def choose_medi(self):
        print("Enter Medication Name: ")
        user_input = input("Input: ")
        fetched_data = self.medi_service.fetch_data()
        ingredients = self.medi_service.find_ingredients(user_input=user_input)
        ingredient = self.medi_service.choose_ingredient(ingredients=ingredients)
        strengths = self.medi_service.find_strengths(ingredient=ingredient)
        strength = self.medi_service.choose_strength(strengths=strengths, ingredient=ingredient)
        found_df = self.medi_service.find_df(ingredient=ingredient, strength=strength)
        print(f"Dosage Form: {found_df}")
        return [ingredient, strength, found_df]


    def choose_carrier_fluid(self):
        carrier_fluids = ["NaCl 0.9%", "Glucose 5%", "Other", "Enter Name"]
        print("Choose a Carrier Fluid: ")
        x = 1
        for fluid in carrier_fluids:
            print(f"-> {x}: {fluid}")
            x += 1
        choice = input("Input: ")
        if carrier_fluids[int(choice) - 1] == carrier_fluids[3]:
            other_fluid = input("Enter Carrier Fluid Name: ")
            return other_fluid
        else:
            carrier_fluid = carrier_fluids[int(choice) - 1]
            return carrier_fluid

    def choose_carrier_volume(self):
        print("Enter the total Infusion Volume [in mL]")
        choice = input("Input: ")
        return choice

    def choose_units(self):
        units = ["1 Unit", "2 Units", "5 Units", "More..."]
        more_units = ["100%", "50%", "25%", "Enter.."]
        print("\n---Enter Units---")
        x = 1
        for unit in units:
            print(f"[ {x}: {unit} ]", sep="  ")
            x += 1
        choice = int(input("Input: "))
        if units[choice - 1] == units[3]:
            x = 1
            for unit in more_units:
                print(f"[ {x}: {unit} ]", sep="  ")
            choice_2 = int(input("Input: "))
            if more_units[choice_2 - 1] == more_units[3]:
                choice_3 = input("\nEnter Unit: ")
                return choice_3
            else:
                return more_units[choice_2 - 1]
        else:
            return units[choice - 1]

    def record_data(self, infusion_recording):
        data_dict = {
                "nurse_id": infusion_recording[0],
                "nurse_name": infusion_recording[1],
                "patient_id": infusion_recording[2],
                "patient_name": infusion_recording[3],
                "medication": infusion_recording[4],
                "strength": infusion_recording[5],
                "dose_format": infusion_recording[6],
                "unit": infusion_recording[7],
                "carrier_fluid": infusion_recording[8],
                "fluid_volume": infusion_recording[9],
                "drops_per_min": infusion_recording[10],
                "ml_per_hour": infusion_recording[11],
                }
        return data_dict
