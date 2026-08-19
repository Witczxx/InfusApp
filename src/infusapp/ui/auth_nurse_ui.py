from infusapp.models.models import NurseInfo
from pwinput import pwinput
import bcrypt

class AuthNurseUi:


    def __init__(self, nurse_service):
        self.nurse_service = nurse_service


    def run(self) -> NurseInfo:
        print("\n---Welcome to the InfusionApp---")

        while True:
            choice: int = self.login_or_register()  # '1' / '2'

            nurse_info: NurseInfo | None = None
            nurse_info = self.login() if choice == 1 else None       # 1 = Login
            nurse_info = self.register() if choice == 2 else None    # 2 = Register

            if nurse_info is not None:
                break

        return nurse_info


    def login_or_register(self) -> int:
        while True:
            print("Enter '1' or '2'")
            print("1: Login as a Nurse")
            print("2: Register as a Nurse")

            choice = input("Your Input: ")  # '1' / '2'

            if choice in ("1", "2"):
                return int(choice)
            else:
                print("Invalid Input. Please enter '1' or '2'")


    def login(self) -> NurseInfo | None:
        print("\n---Nurse Login---")

        while True:
            user_input = input("Enter Name or ID: ")
            pw = pwinput(prompt="Password: ", mask="*")
            login: bool = self.nurse_service.login(user_input=user_input, pw=pw)
            ... # CHECK NURSE SERVICE
                




            kind: str = self.validate_input(user_input = user_input)    # "nurse_id" / "nurse_name" / "not_found"
            if kind == "not_found":
                print("Login failed"); continue
            elif kind == "nurse_id":
                nurse_id: int = int(user_input)
                nurse_name: str = self.nurse_service.get_nurse_name_by_id(nurse_id=nurse_id)
            elif kind == "nurse_name":
                nurse_name: str = user_input
                nurse_id: int = self.nurse_service.get_nurse_id_by_name(nurse_name=nurse_name)
            else:
                print("Unexpected Problem during Input Validation"); continue



    def validate_input(self, user_input: str) -> str: 
        is_id: bool = self.nurse_service.val_nurse_id(nurse_id=user_input)
        is_name: bool = self.nurse_service.val_nurse_name(nurse_name=user_input)
        return "nurse_id" if is_id else ("nurse_name" if is_name else "not_found")


# ------------------------------------------


        # Nurse ID was entered
        if self.nurse_service.val_nurse_id(user_input):
            nurse_id = user_input
            try:
                actual_nurse = self.nurse_service.login_nurse(nurse_id=nurse_id, pw=pw)
            except ValueError as errormessage:
                print(errormessage)
                return self.start_screen()
        # Nurse Name was entered
        elif self.nurse_service.val_nurse_name(user_input.title()):
            nurse_name = user_input.title()
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
        self.actual_nurse.append(actual_nurse)  # Logged in Nurse Name
        return actual_nurse


# ------------------------------------------


    ### REGISTRATION SCREEN (2)
    def register(self):
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
                print(f"Your ID is: {new_nurse[0]}")
                print("Please note down your ID")
                return self.login_screen()
        else:
            print("Password inputs are not identical.")
            return self.register_screen()
