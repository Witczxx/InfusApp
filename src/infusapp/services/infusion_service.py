from sqlite3 import Row

class InfusionService:
    def __init__(self, infusion_rep):
        self.infusion_rep = infusion_rep

    def add_to_db(self, nurse, patient, medi) -> None:
        self.infusion_rep.add_to_db(
            nurse=nurse, patient=patient, medi=medi
        )
