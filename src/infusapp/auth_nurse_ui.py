from infusapp.nurse_service import NurseService
from infusapp.home_ui import HomeUi

class AuthNurseUi:
    def __init__(self):
        self.actual_nurse = None
        self.nurse_service = NurseService()

    ### START SCREEN
    def start_screen(self):
        print("\n\n\n---Welcome to the InfusionApp---")
        print("Enter '1' or '2'\n1: Login as a Nurse\n2: Register as a Nurse")
        choice = input("Your Input: ")
        # Enter 1 (Login) or 2 (Registration)
        if choice == "1":
            return self.login_screen()
        elif choice == "2":
            return self.register_screen()
        # No 0/1
        else:
            print("Input is not '1' or '2'")
            return self.start_screen()

    ### LOGIN SCREEN (1)
    def login_screen(self):
        print("\n---Nurse Login---")
        # Define Variables
        nurse_id = None
        nurse_name = None
        # Enter Name or ID, and Password
        user_input = input("Enter Name or ID: ").title()
        pw = input("Password: ")
        # Nurse ID was entered
        if self.nurse_service.val_nurse_id(user_input):
            nurse_id = user_input
            try:
                actual_nurse = self.nurse_service.login_nurse(nurse_id=nurse_id, pw=pw)
            except ValueError as errormessage:
                print(errormessage)
                return self.start_screen()
        # Nurse Name was entered
        elif self.nurse_service.val_nurse_name(user_input):
            nurse_name = user_input
            try:
                actual_nurse = self.nurse_service.login_nurse(nurse_name=nurse_name, pw=pw)
            except ValueError as errormessage:
                print(errormessage)
                return self.start_screen()
       # When neither ID or Name recognized
        else:
            print("Name, ID or Password wrong.")
            return self.start_screen()
        # Login was Successful!
        self.actual_nurse = actual_nurse  # Logged in Nurse Name
        home_ui = HomeUi(self.actual_nurse)
        return home_ui.home_screen(nurse_name=actual_nurse)

    ### REGISTRATION SCREEN (2)
    def register_screen(self):
        print("\n---Nurse Registration---")
        # Enter Name and (2x) Password
        nurse_name = input("Name (First, Last): ")
        pw = input("Password: ")
        rpw = input("Repeat Password: ")
        # Send Registration Data to HIS
        if pw == rpw:
            try:
                new_nurse = self.nurse_service.register_nurse(nurse_name, pw)
            except ValueError as errormessage:
                print(errormessage)
                return self.register_screen()
            else:
                print("\n---Registration Successful!---")
                print(f"---Your ID is: {new_nurse.nurse_id}---")
                print("Please note down your ID")
                return self.login_screen()
        else:
            print("Password inputs are not identical.")
            return self.register_screen()
