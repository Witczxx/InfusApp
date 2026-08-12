import random
import sys

# DATABASES
nurse_data = [{"ID": "1000000", "Name": "Max Mustermann", "Password": "max10"}]
patient_data = {}
doctor_data = {}


def nurse_registration_or_login():
    choice = input("Enter '1' or '2'\n1: Login as a Nurse\n2: Register as a Nurse")
    if choice == "1":
        return nurse_login()
    elif choice == "2":
        return nurse_registration()
    else:
        sys.exit("Input is not '1' or '2'")


def nurse_login():
    print("\n---Nurse Login---")
    n_name_id = input("Enter Name or ID: ")
    n_pw = input("Password: ")
    key = "ID" if n_name_id.isdigit() else "Name"
    return check_nurse_registration_login(
        {
            key: n_name_id,
            "Password": n_pw,
        }
    )


def nurse_registration():
    print("\n---Nurse Registration---")
    n_name = input("Name (First, Last): ")
    n_id = random.randrange(1000000, 9999999)
    n_pw = input("Password: ")
    n_rpw = input("Repeat Password: ")
    if n_pw == n_rpw:
        return check_nurse_registration_login(
            {
                "ID": n_id,
                "Name": n_name,
                "Password": n_pw,
            }
        )
    else:
        print("Password inputs are not identical.")
        nurse_registration()


def check_nurse_registration_login(input_nurse_data): ...


def main():
    print("\n---Welcome to the InfusionApp---")
    input_nurse_data = nurse_registration_or_login()
    check_nurse_registration_login(input_nurse_data)


if __name__ == "__main__":
    main()
