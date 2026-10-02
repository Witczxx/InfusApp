from infusapp.exceptions.exceptions import DocumentationAborted
from sqlite3 import Row

class MediUiHelper:


    def get_ingredients_input_data(self, medi_service) -> tuple:
        user_input = input("Input: ").upper()
        if user_input == 'Q':
            raise DocumentationAborted()
        fetched_data: list[Row] = medi_service.fetch_data(user_input=user_input)
        return fetched_data, user_input


    def get_ingredients_list(
        self, medi_service, fetched_data: list[Row], user_input: str
    ) -> list | None:
        ingredients_list: list | None = medi_service.filter_ingredients_by_route(
            user_input=user_input, fetched_data=fetched_data
        )
        return ingredients_list


    def choose_ingredient_input(self, ingredients_list: list) -> str:
        for index, ingredient in enumerate(ingredients_list):
            print(f"-> {index + 1}: {ingredient}")
        while True:
            try:
                ingredient_input = input("Input: ")
                if ingredient_input.lower() == 'q':
                    raise DocumentationAborted()
                int_ingredient_input = int(ingredient_input) - 1
                if int_ingredient_input  >= 0 and int_ingredient_input < len(ingredients_list):
                    break
                else:
                    print("Please choose a number in the given range.")
            except ValueError:
                print("Input is not a number")
        return ingredients_list[int_ingredient_input]


    def choose_strength_input(self, strengths) -> str:
        for index, strength in enumerate(strengths):
            print(f"-> {index + 1}: {strength}")
        while True:
            try:
                strength_input = input("Input: ")
                if strength_input.lower() == 'q':
                    raise DocumentationAborted()
                strength_input = int(strength_input) - 1
                if strength_input >= 0 and strength_input < len(strengths):
                    break
                else:
                    print("Please choose a number in the given range.")
            except ValueError:
                print("Input is not a number.")
        return strengths[strength_input]

    def choose_units_choice_1(self, units: list) -> int:
        for index, unit in enumerate(units):
            print(f"[ {index + 1}: {unit} ]", sep="  ")
        while True:
            choice_1 = input("Input: ")
            if choice_1 in ["1", "2", "3", "4"]:
                choice_1 = int(choice_1) - 1
                return choice_1
            else:
                print("Please enter '1', '2', '3' or '4'")

    def choose_units_choice_2(self, units: list, more_units: list) -> int:
        for index, unit in enumerate(more_units):
            print(f"[ {index + 1}: {unit} ]", sep="  ")
        while True:
            choice_2 = input("Input: ")
            if choice_2 in ["1", "2", "3", "4"]:
                choice_2 = int(choice_2) - 1
                return choice_2
            else:
                print("Please enter '1', '2', '3', or '4'")

    def choose_units_choice_3(self) -> int:
        while True:
            try:
                choice_3 = int(input("\nEnter Unit: "))
                if choice_3 > 0 and choice_3 < 9999999:
                    return choice_3
                else:
                    print("Input has an uncommon number.")
            except ValueError:
                print("Input is not a number.")

    def ask_if_carrier_fluid_needed(self) -> bool:
        print("\n---Is a Carrier Fluid being added? (y/n)---")
        while True:
            ask_carrier_fluid = input("Input: ").strip().lower()
            if ask_carrier_fluid == "y":
                return True
            elif ask_carrier_fluid == "n":
                print("---Selection Completed---")
                return False
            else:
                print("Input not recognized. Enter 'y' or 'n'")

    def choose_carrier_fluid_input(self, carrier_fluids: list) -> int:
        for index, fluid in enumerate(carrier_fluids):
            print(f"-> {index}: {fluid}")
        while True:
            choice = input("Input: ")
            if choice.lower() == 'q':
                raise DocumentationAborted()
            if choice in ["1", "2", "3", "4"]:
                return int(choice) - 1
            else:
                print("Input is no number.")
