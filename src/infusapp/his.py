import random
import re

from model import Nurse


class His:
    def __init__(self):
        self.nurses = []
        self.nurses.append(Nurse("1000000", "Max Mustermann", "max10"))

    ### REGISTRATION
    def register(self, nurse_name, pw):
        # Is the Name valid?
        if not self.val_nurse_name(nurse_name):
            raise ValueError(
                "Invalid Nurse Name.\nEnter your first and last name (e.g. Max Mustermann)"
            )
        # Is the Name taken?
        if self.nurse_name_exists(nurse_name):
            raise ValueError("This name is already taken")
        # Is the Password valid?
        if not self.val_pw(pw):
            raise ValueError(
                "Invalid Password\nEnter a password with 8 - 32 characters"
            )
        # Generate a Unique ID
        nurse_id = self.generate_nurse_id()
        # Add User to the Database
        new_nurse = Nurse(nurse_id, nurse_name, pw)
        self.nurses.append(new_nurse)
        return new_nurse

    ### LOGIN
    def login(self, pw, nurse_id=None, nurse_name=None):
        # Does ID exist?
        if nurse_id is not None:
            if not self.nurse_id_exists(nurse_id):
                raise ValueError("This ID does not exist")
            nurse_name = self.get_nurse_name_by_id(nurse_id)
        # Does Name exist?
        elif nurse_name is not None:
            if not self.nurse_name_exists(nurse_name):
                raise ValueError("This Name does not exist")
            nurse_id = self.get_nurse_id_by_name(nurse_name)
        # Is the Password Valid?
        if not self.verify_pw(nurse_id, pw):
            raise ValueError("ID exists, but wrong Password")
        return nurse_name

    ### FUNCTIONS FOR NURSE NAME
    # Generate ID
    def generate_nurse_id(self):
        while True:
            nurse_id = str(random.randrange(1000000, 9999999))
            for nurse in self.nurses:
                if nurse_id == nurse.nurse_id:
                    break
            else:
                return nurse_id

    # Is ID Valid?
    def val_nurse_id(self, nurse_id):
        if match := re.search(r"^[0-9]{7}$", nurse_id.strip()):
            return True
        else:
            return False

    # Is ID Taken?
    def nurse_id_exists(self, nurse_id):
        for nurse in self.nurses:
            if nurse_id == nurse.nurse_id:
                return True
        return False

    # Find ID with Nurse Name
    def get_nurse_name_by_id(self, nurse_id):
        for nurse in self.nurses:
            if nurse_id == nurse.nurse_id:
                return nurse.nurse_name

    ### FUNCTIONS FOR NURSE NAME
    # Is Name Valid?
    def val_nurse_name(self, nurse_name):
        return bool(re.search(r"^[a-zA-Z]{2,16} [a-zA-Z]{2,16}$", nurse_name.strip()))

    # Is Name Taken?
    def nurse_name_exists(self, nurse_name):
        for nurse in self.nurses:
            if nurse_name == nurse.nurse_name:
                return True

    # Find Name with ID
    def get_nurse_id_by_name(self, nurse_name):
        for nurse in self.nurses:
            if nurse_name == nurse.nurse_name:
                return nurse.nurse_id

    ### FUNCTIONS FOR PASSWORDS
    # Is Password Valid?
    def val_pw(self, pw):
        return bool(re.search(r"^.{8,32}$", pw))

    # Does Password fit to ID/Name ?
    def verify_pw(self, nurse_id, pw):
        for nurse in self.nurses:
            if nurse_id == nurse.nurse_id and pw == nurse.pw:
                return True
