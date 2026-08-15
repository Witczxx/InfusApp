import sys

from infusapp.record_infusion_ui import RecordInfusion

class HomeUi:

    def __init__(self, actual_nurse):
        self.actual_nurse = actual_nurse

    ### HOME SCREEN - LOGIN SUCCESSFUL
    def home_screen(self, nurse_name):
        print(f"\n\n\n---Welcome, {self.actual_nurse}---")
        print("\n---Home Screen---\nEnter '1', '2', '3' or '4'")
        print("1: Record an Infusion\n2: Check your Infusion Records\n3: How the App works\n4: Logout and Exit")
        choice = input("Your Input: ")
        # Record an Infusion (1)
        if choice == "1": 
            record_infusion = RecordInfusion(self.actual_nurse)
            return record_infusion.record_infusion_ui()
        # Check Infusion Records (2)
        elif choice == "2":
            return None     # Coding in Progress
        # How the App Works (3)
        elif choice == "3":
            with open("app_explanation.md", "r") as file:
                print(f"\n\n\n{file.read()}")
                input("\n---Press any key to return to the Home Screen---")
                return self.home_screen(self.actual_nurse)
        # Logout and Exit (4)
        elif choice == "4":
            sys.exit("\n\n---Goodbye! Looking forward to see you soon!---")
        # If not entered 1/2/3/4
        else:
            print("Input is not '1', '2', '3' or '4'")
            return self.home_screen(self.actual_nurse)
