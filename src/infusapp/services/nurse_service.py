import random
import re
from sqlite3 import Row

import bcrypt

from infusapp.db.nurse_repository import NurseRepository
from infusapp.models.models import Nurse


class NurseService:

    def __init__(self, nurse_rep: NurseRepository):
        self.nurse_rep = nurse_rep

    def login(self, user_input: str, pw: str) -> Nurse | None:
        user_input = user_input.strip()
        match: Row | None = self.nurse_rep.search_by_input(user_input=user_input)
        val_pw: bool = (
            self.ver_pw(pw=pw, hashed_pw=match["hash_pw"])
            if match is not None
            else False
        )
        return (
            Nurse(nurse_id=match["nurse_id"], nurse_name=match["nurse_name"])
            if val_pw and match is not None
            else None
        )

    def registration(self, nurse_name: str, pw: str) -> Nurse | None:
        nurse_name = nurse_name.strip().title()
        match: Row | None = self.nurse_rep.search_by_input(user_input=nurse_name)
        if (
            match is not None
            or not self.val_pw(pw=pw)
            or not self.val_name(search_value=nurse_name)
        ):
            return None
        nurse_id: int = self.generate_nurse_id()
        hash_pw: str = self.hash_pw(pw=pw)
        reg_nur: Row | None = self.nurse_rep.add_to_db(
            nurse_id=nurse_id, nurse_name=nurse_name, hash_pw=hash_pw
        )
        return (
            Nurse(nurse_id=reg_nur["nurse_id"], nurse_name=reg_nur["nurse_name"])
            if reg_nur is not None
            else None
        )

    def val_name(self, search_value: str) -> bool:
        return bool(re.search(r"^[\w]{2,16} [\w]{2,16}$", search_value.strip()))

    def val_pw(self, pw: str) -> bool:
        return bool(re.search(r"^.{8,32}$", pw))

    def hash_pw(self, pw: str) -> str:
        return bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()

    def ver_pw(self, pw: str, hashed_pw: str) -> bool:
        return bcrypt.checkpw(pw.encode(), hashed_pw.encode())

    def generate_nurse_id(self):
        while True:
            id: int = random.randrange(start=1000000, stop=9999999)
            id_exists: Row | None = self.nurse_rep.search_by_input(user_input=str(id))
            if not id_exists:
                return id
