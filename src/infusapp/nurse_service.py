import random
import re
from dataclasses import dataclass

from infusapp.model import Nurse
from infusapp.service_helper import check_existence, find_by_value, val_name, generate_id


@dataclass
class NurseInfo:
    nurse_id: str
    nurse_name: str


class NurseService:
    def __init__(self):
        self.nurses = []
        self.nurses.append(
            Nurse(nurse_id="1000000", nurse_name="Max Mustermann", pw="max10")
        )

    ### LOGIN
    def login_nurse(self, pw, nurse_id=None, nurse_name=None):
        # ID exists?
        if nurse_id is not None:
            if not self.nurse_id_exists(nurse_id=nurse_id):
                raise ValueError("\n---Name, ID or Password wrong.---")
            nurse_name = self.get_nurse_name_by_id(nurse_id=nurse_id)
        # Name exists?
        elif nurse_name is not None:
            if not self.nurse_name_exists(nurse_name=nurse_name):
                raise ValueError("\n---Name, ID or Password wrong.---")
            nurse_id = self.get_nurse_id_by_name(nurse_name=nurse_name)
        # PW valid?
        if not self.verify_pw(nurse_id=nurse_id, pw=pw):
            raise ValueError("\n---Name, ID or Password wrong.---")
        # Login Successful
        return nurse_id, nurse_name

    ### REGISTRATION
    def register_nurse(self, nurse_name, pw):
        # Name valid?
        if not self.val_nurse_name(nurse_name=nurse_name):
            raise ValueError(
                "\n---Invalid Nurse Name---\nEnter your first and last name (e.g. Max Mustermann)"
            )
        # Name taken?
        if self.nurse_name_exists(nurse_name=nurse_name):
            raise ValueError("\n---This name is already taken---")
        # PW valid?
        if not self.val_pw(pw):
            raise ValueError(
                "\n---Invalid Password---\nEnter a password with 8 - 32 characters"
            )
        # Generate ID
        nurse_id = self.generate_nurse_id()
        # Add to Database
        new_nurse = Nurse(nurse_id=nurse_id, nurse_name=nurse_name, pw=pw)
        self.nurses.append(new_nurse)
        return nurse_id, nurse_name
        return NurseInfo(nurse_id=new_nurse.nurse_id, nurse_name=new_nurse.nurse_name)
        # Need some Correction

    ### FUNCTIONS

    # PW VALID?
    def val_pw(self, pw):
        return bool(re.search(r"^.{8,32}$", pw))

    # VERIFY PW
    def verify_pw(self, nurse_id, pw):
        for nurse in self.nurses:
            if nurse_id == nurse.nurse_id and pw == nurse.pw:
                return True
        return False

    # ID VALID?
    def val_nurse_id(self, nurse_id):
        return bool(re.search(r"^[0-9]{7}$", nurse_id.strip()))

    # NAME VALID?
    def val_nurse_name(self, nurse_name):
        return bool(re.search(r"^[a-zA-Z]{2,16} [a-zA-Z]{2,16}$", nurse_name.strip()))

    # ID EXISTS?
    def nurse_id_exists(self, nurse_id):
        return check_existence(
            entries=self.nurses, field_name="nurse_id", search_value=nurse_id
        )

    # NAME EXISTS?
    def nurse_name_exists(self, nurse_name):
        return check_existence(
            entries=self.nurses, field_name="nurse_name", search_value=nurse_name
        )

    # FIND ID [No Shortening, Helper would return Password]
    def get_nurse_id_by_name(self, nurse_name):
        for nurse in self.nurses:
            if nurse_name == nurse.nurse_name:
                return nurse.nurse_id
        else:
            return None

    # FIND NAME [No Shortening, Helper would return Password]
    def get_nurse_name_by_id(self, nurse_id):
        for nurse in self.nurses:
            if nurse_id == nurse.nurse_id:
                return nurse.nurse_name
        else:
            return None

    # GENERATE ID
    def generate_nurse_id(self):
        return generate_id(self.nurses, "nurse_id", 1000000, 9999999)
