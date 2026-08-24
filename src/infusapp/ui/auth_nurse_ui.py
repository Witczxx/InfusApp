from pwinput import pwinput

from infusapp.models.models import Nurse


class AuthNurseUi:

    def __init__(self, nurse_service):
        self.nurse_service = nurse_service

    def run(self) -> Nurse:
        print("\n---Welcome to the InfusionApp---")
        while True:
            choice: int = self.login_or_register()  # '1' / '2'
            nurse_info: Nurse | None = None
            if choice == 1:  # 1 = Login
                nurse_info = self.login_nurse()
            elif choice == 2:  # 2 = Register
                nurse_info = self.register_nurse()
            else:
                nurse_info = None
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

    def login_nurse(self) -> Nurse | None:
        print("\n---Nurse Login---")
        user_input = input("Enter Name or ID: ")
        pw = pwinput(prompt="Password: ", mask="*")
        login: Nurse | None = self.nurse_service.login(user_input=user_input, pw=pw)
        (
            print("\n---Login Successful---")
            if login is not None
            else print("\n---Login Failed---")
        )
        return login

    def register_nurse(self) -> Nurse | None:
        print("\n---Nurse Registration---")
        nurse_name = input("Name (First, Last): ")
        pw = pwinput(prompt="Password: ", mask="*")
        rpw = pwinput(prompt="Repeat Password: ", mask="*")
        if pw == rpw:
            register: Nurse | None = self.nurse_service.registration(
                nurse_name=nurse_name, pw=pw
            )
            if register is not None:
                print("\n---Registration Successful!---")
                print(f"Your ID is: {register.nurse_id}\nPlease not down your ID")
                return register
        print("\n---Registration Failed---")
        return None
