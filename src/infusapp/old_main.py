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
        return nurse_registration()


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


def check_nurse_registration_login(input_nurse_data):
    # Registration
    if len(input_nurse_data) == 3:
        if not input_nurse_data == nurse_data[0]:
            print("---Registration Successful---")
            nurse_data.append(input_nurse_data)
            return nurse_login()
        else:
            print("--Registration Failed--\nPlease try again.")
            return nurse_registration()
    # Login
    elif len(input_nurse_data) == 2:
        key = "ID" if "ID" in input_nurse_data else "Name"
        for nurse in nurse_data:
            if input_nurse_data[key] == nurse[key] and input_nurse_data["Password"] == nurse["Password"]:
                print("---Login Successful---")
                return infuapp_home()
        print("\n---Login Failed---\nPlease try again")
        return nurse_login()
    else:
        sys.exit("WEIRD: Nurse Login or Registration Output Error")


def infuapp_home():
    return print("We made it to InfuApp!")

def main():
    print("\n---Welcome to the InfusionApp---")
    nurse_registration_or_login()


if __name__ == "__main__":
    main()
