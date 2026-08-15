import json
import re

class Medication_Db:
    ### FUNCTIONS FOR MEDICATION
    def __init__(self, filepath):
        with open("drug-ndc-0001-of-0001.json", "r") as file:
            self.data = json.load(file)

    # Get Access to Database

    # Login
    def medi_login(self): ...

    # Name Valid?
    def val_medi_name(self): ...

    # ID Valid?
    def val_medi_id(self): ...

    # Name Exists?
    def medi_name_exists(self): ...

    # ID Exists?
    def medi_id_exists(self): ...



    for medi in self.data.get("results", []):
        # Route and Dosage Form
        routes = medi.get("route", [])
        routes = ", ".join(routes) if routes else "Unknown"
        dosage_form = medi.get("dosage_form", "")
        # Medi Group Data (Brand Name, Generic Name, NDC)
        brand_name = medi.get("brand_name", "Unknown")
        generic_name = medi.get("generic_name", "Unknown")
        product_ndc = medi.get("product_ndc")
        # Medi Group RXCUI
        openfda = medi.get("openfda", {})
        rxcui = openfda.get("rxcui", [None])[0]
        # Active Ingredients Data (Strengths, Medi Names)
        ingredients = [
            f"{ing.get('name')}: {ing.get('strength', 'No Information')}"
            for ing in medi.get("active_ingredients", [])
        ]
        # Packages Data (NDC, Description)
        packages = []
        for pkg in medi.get("packaging", []):
            pkg_des_raw = pkg.get("description", "Unknown")
            segments = pkg_des_raw.split("/")
            for segment in segments:
                segment = segment.strip()
                if match := re.search(r"^(?P<des>[^(]+)\s*(\((?P<ndc>[0-9-]+)\))?$", segment):
                    packages.append({
                        "ndc": match.group("ndc"),
                        "description": match.group("des").strip(),
                    })
        # Output
        print(f"Brand: {brand_name} | Generic: {generic_name}")
        print(f"Dosage Form: {dosage_form} | Route: {routes}")
        print(f"NDC: {product_ndc} | RxCUI: {rxcui}")
        print(f"Strengths: {', '.join(ingredients)}")
        print("-" * 25)
        print("Packages:")
        for package in packages:
            print(f"----------\nNDC: {package['ndc']}\nDescription: {package['description']}")
        print("-" * 50)
