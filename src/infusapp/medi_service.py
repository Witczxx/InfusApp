import re
import sqlite3

from tabulate import tabulate

from infusapp.medi_db import MediDb


class MediService:

    def __init__(self, medi_db):
        self.medi_db = medi_db
        self.data = []
        self.filtered_data = []

    def fetch_data(self):
        # Get Data from Databank
        self.medi_db.cur.execute("""
                                 SELECT ingredient, df, strength, route, trade_name
                                 FROM medications
                                 """)
        # Fetch Findings into a Variable
        self.data = self.medi_db.cur.fetchall()
        return self.data

    def find_ingredients(self, user_input):
        # Filter Unique Findings (all headers) ; filtered by IV/INJECTION
        data_set = set()
        for finding in self.data:
            if "INTRAVENOUS" in finding[3] or "INJECTION" in finding[3]:
                if any(user_input in str(string) for string in finding):
                    data_set.add(finding)
        self.filtered_data = data_set
        # filter unique data[0]
        found_ingredients = list({data[0] for data in data_set})
        # sort alphabetically
        return sorted(found_ingredients)

    def choose_ingredient(self, ingredients):
        # Let User Choose Ingredient
        if len(ingredients) > 1:
            print(f"\n---{len(ingredients)} Ingredients found---")
            print("Choose the correct Ingredient")
            x = 1
            for ingredient in ingredients:
                print(f"-> {x}: {ingredient}")
                x += 1
            ingredient_input = int(input("Input: "))
            chosen_ingredient = ingredients[ingredient_input - 1]
            print(f"\n---Your Choice---\nIngredient: {chosen_ingredient}")
        else:
            chosen_ingredient = ingredients[0]
            print(f"\n---1 Ingredient Found---")
            print("---Automatically Chosen---")
            print("---Your Choice---")
            print(f"Ingredient: {chosen_ingredient}")
        return chosen_ingredient

    def find_strengths(self, ingredient):
        # filter unique strengths by chosen data[0]
        found_strengths = list({data[2] for data in self.filtered_data if data[0] == ingredient})
        # sort by numbers (first appearing, second appearing, ..)
        sorted_strengths = sorted(found_strengths, key=self.strengths_sort_key)
        return sorted_strengths

    def choose_strength(self, strengths, ingredient):
        # Let User Choose Strength
        if len(strengths) > 1:
            print(f"\n---{len(strengths)} Strengths found---")
            print("Choose the correct Strength")
            x = 1
            for strength in strengths:
                print(f"-> {x}: {strength}")
                x += 1
            strength_input = int(input("Input: "))  # NEED IMPROVEMENT
            strength = strengths[strength_input - 1]
            print(f"\n---Your Choice---")
            print(f"Ingredient: {ingredient}")
            print(f"Strength: {strength}")
            return strength
        else:
            strength = strengths[0]
            print(f"\n---1 Strength found---")
            print("---Automatically Chosen---")
            print(f"Ingredient: {ingredient}")
            print(f"Strength: {strength}")
            return strength

    def find_df(self, ingredient, strength):
        final_findings = [
            finding
            for finding in self.data
            if finding[0] == ingredient and finding[2] == strength
        ]
        if not final_findings:
            return "Unknown"
        df_values = sorted({finding[1] for finding in final_findings})
        return " | ".join(df_values)

    def strengths_sort_key(self, strengths):
        matches = re.findall(r"\d+", strengths)
        return tuple(int(n) for n in matches)
