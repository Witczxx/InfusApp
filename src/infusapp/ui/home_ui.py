import sys
from pathlib import Path

from infusapp.exceptions.exceptions import DocumentationAborted

class HomeUi:

    def __init__(self, nurse, new_infusion_ui, record_ui, expl_path=None):
        self.nurse = nurse
        self.new_infusion_ui = new_infusion_ui
        self.record_ui = record_ui
        self.expl_path = expl_path or Path(__file__).parent.parent.parent.parent / "docs" / "app_explanation.md"

    def run(self) -> None:
        while True:
            print("\n---Home Screen---")
            choice: int = self.choose_one_to_four()
            if choice == 1:
                try:
                    self.new_infusion_ui.run()
                except DocumentationAborted:
                    print("\n---Recording aborted---")
            elif choice == 2:
                self.record_ui.run(nurse=self.nurse)
            elif choice == 3:
                self.app_explanation()
            elif choice == 4:
                return sys.exit("\n---Logged Out---\n---App Closed---")
            else:
                print("Input is not '1', '2', '3' or '4'")

    def choose_one_to_four(self) -> int:
        while True:
            print("\nEnter '1', '2', '3' or '4'")
            print("1: Record an Infusion")
            print("2: Check your Infusion Records")
            print("3: How the App works")
            print("4: Logout and Exit")
            choice = input("Your Input: ")
            if choice in ("1", "2", "3", "4"):
                return int(choice)
            else:
                print("Invalid Input. Please enter a number between '1' and '4'")

    def app_explanation(self) -> None:
        with open(self.expl_path, "r") as file:
            print(f"\n\n\n{file.read()}")
            input("\n---Press any key to return to the Home Screen---")
