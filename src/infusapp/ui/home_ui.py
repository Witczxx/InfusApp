import sys
from pathlib import Path


class HomeUi:

    def __init__(self, actual_nurse):
        self.actual_nurse = actual_nurse

    ### InfusApp - Main Menu
    def show_menu(self):
        print("\n---Home Screen---\nEnter '1', '2', '3' or '4'")
        print(
            "1: Record an Infusion\n2: Check your Infusion Records\n3: How the App works\n4: Logout and Exit"
        )
        choice = input("Your Input: ")
        # Record an Infusion (1)
        if choice == "1":
            return "Record Infusion"
        # Check Infusion Records (2)
        elif choice == "2":
            return "Check Records"  # Coding in Progress
        # How the App Works (3)
        elif choice == "3":
            path = Path(__file__).parent / "app_explanation.md"
            with open(path, "r") as file:
                print(f"\n\n\n{file.read()}")
                input("\n---Press any key to return to the Home Screen---")
                return self.show_menu()
        # Logout and Exit (4)
        elif choice == "4":
            return "Logout and Exit"
        # If not entered 1/2/3/4
        else:
            print("Input is not '1', '2', '3' or '4'")
            return self.show_menu()
