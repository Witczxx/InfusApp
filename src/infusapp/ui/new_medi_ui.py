from datetime import datetime
from sqlite3 import Row

from infusapp.infusion_tracker.infusion_tracker import InfusionTracker
from infusapp.models.models import Medi
from infusapp.services.medi_service import MediService
from infusapp.ui.medi_ui_helper import MediUiHelper


class NewMediUi:

    def __init__(self, medi_service: MediService):
        self.medi_service = medi_service
        self.infusion_tracker = InfusionTracker()
        self.medi_ui_helper = MediUiHelper()

    def run(self) -> Medi:
        ingredients_list: list = self.get_ingredients()
        chosen_ingredient: str = self.choose_ingredient(
            ingredients_list=ingredients_list
        )
        strength: str = self.choose_strength(chosen_ingredient=chosen_ingredient)
        dosage_form: str = self.medi_service.find_df(
            chosen_ingredient=chosen_ingredient, strength=strength
        )
        unit: int | float = self.choose_units()
        carrier_fluid: str | None = self.choose_carrier_fluid()
        total_volume: int = self.choose_total_volume()
        drops_per_min: int
        ml_per_hour: int
        drops_per_min, ml_per_hour = self.track_infusion()
        start_time: datetime
        stop_time: datetime
        start_time, stop_time = self.medi_service.calculate_datetimes(
            total_volume=total_volume, ml_per_hour=ml_per_hour
        )
        return Medi(
            ingredient=chosen_ingredient,
            strength=strength,
            unit=unit,
            dosage_form=dosage_form,
            carrier_fluid=carrier_fluid,
            total_volume=total_volume,
            drops_per_min=drops_per_min,
            ml_per_hour=ml_per_hour,
            start_time=start_time,
            stop_time=stop_time,
        )

    def get_ingredients(self) -> list:
        print("\n---Choose Medication---")
        print("Enter Medication Name: ")
        print("(press 'q' to return to the home menu)")
        while True:
            fetched_data: list[Row]
            ingredients_list: list | None = None
            fetched_data, user_input = self.medi_ui_helper.get_ingredients_input_data(
                medi_service=self.medi_service
            )
            if fetched_data:
                ingredients_list = self.medi_ui_helper.get_ingredients_list(
                    medi_service=self.medi_service,
                    fetched_data=fetched_data,
                    user_input=user_input,
                )
            if ingredients_list is not None:
                return ingredients_list
            else:
                print("\nMedication not found. Please try again.")

    def choose_ingredient(self, ingredients_list: list) -> str:
        if len(ingredients_list) > 1:
            print(f"\n---{len(ingredients_list)} Ingredients found---")
            print("Choose the correct Ingredient")
            print("(press 'q' to return to the home menu)")
            chosen_ingredient: str = self.medi_ui_helper.choose_ingredient_input(
                ingredients_list=ingredients_list
            )
            print(f"\n---Your Choice---\nIngredient: {chosen_ingredient}")
        else:
            chosen_ingredient = ingredients_list[0]
            print(f"\n---1 Ingredient Found---")
            print("---Automatically Chosen---")
            print("---Your Choice---")
            print(f"Ingredient: {chosen_ingredient}")
        return chosen_ingredient

    def choose_strength(self, chosen_ingredient):
        strengths = self.medi_service.find_strengths(
            chosen_ingredient=chosen_ingredient
        )
        if len(strengths) > 1:
            print(f"\n---{len(strengths)} Strengths found---")
            print("Choose the correct Strength")
            print("(press 'q' to return to the home menu)")
            strength = self.medi_ui_helper.choose_strength_input(strengths=strengths)
            print(f"\n---Your Choice---")
            print(f"Ingredient: {chosen_ingredient}")
            print(f"Strength: {strength}")
            return strength
        else:
            strength = strengths[0]
            print(f"\n---1 Strength found---")
            print("---Automatically Chosen---")
            print(f"Ingredient: {chosen_ingredient}")
            print(f"Strength: {strength}")
            return strength

    def choose_units(self) -> int | float:
        print("\n---Choose Units---")
        print("(press 'q' to return to the home menu)")
        units = ["1 Unit", "2 Units", "5 Units", "More..."]
        units_int = [1, 2, 5]
        more_units = ["100%", "50%", "25%", "Enter.."]
        more_units_int = [1, 0.5, 0.25]
        print("\n---Enter Units---")
        choice_1: int = self.medi_ui_helper.choose_units_choice_1(units=units)
        if units[choice_1] != units[3]:
            print(f"\nChosen Unit: {units[choice_1]}")
            return units_int[choice_1]
        else:
            choice_2: int = self.medi_ui_helper.choose_units_choice_2(
                units=units, more_units=more_units
            )
            if more_units[choice_2] != more_units[3]:
                print(f"\nChosen Unit: {more_units[choice_2]}")
                return more_units_int[choice_2]
            else:
                choice_3: int = self.medi_ui_helper.choose_units_choice_3()
                print(f"\nChosen Unit: {choice_3}")
                return choice_3

    def choose_carrier_fluid(self) -> str | None:
        fluid_needed: bool = self.medi_ui_helper.ask_if_carrier_fluid_needed()
        if not fluid_needed:
            return None
        carrier_fluids: list = ["NaCl 0.9%", "Glucose 5%", "Other", "Enter Name"]
        print("Choose a Carrier Fluid: ")
        print("(press 'q' to return to the home menu)")
        choice = self.medi_ui_helper.choose_carrier_fluid_input(
            carrier_fluids=carrier_fluids
        )
        if carrier_fluids[choice] == carrier_fluids[3]:
            other_fluid = input("Enter Carrier Fluid Name: ")
            return other_fluid
        else:
            carrier_fluid = carrier_fluids[choice]
            return carrier_fluid

    def choose_total_volume(self) -> int:
        print("Enter the total Infusion Volume [in mL]")
        print("(press 'q' to return to the home menu)")
        while True:
            try:
                choice = int(input("Input: "))
                if choice > 0 and choice <= 1000:
                    return choice
                else:
                    print("Please choose a number in the given Range (1-1000).")
            except ValueError:
                print("Input is not a number")

    def track_infusion(self) -> tuple:
        while True:
            recording: tuple | None = self.infusion_tracker.menu()
            if recording:
                drops_per_min, ml_per_hour = recording
                return drops_per_min, ml_per_hour
            else:
                print("Not enough Data. Please record again.")
