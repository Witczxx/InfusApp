from validation+models import Nurse


class NurseAuth:
    def __init__(self, nurses):
        self.nurses = nurses

    def login(self, n_id, pw):
        ...

    def register(self, id, name, password):

