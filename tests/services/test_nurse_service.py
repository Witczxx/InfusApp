def test_login_id_success(nurse_service, anna):
    result = nurse_service.login(user_input=str(anna["nurse"].nurse_id), pw=anna["pw"])
    assert result.nurse_id == anna["nurse"].nurse_id
    assert result.nurse_name == anna["nurse"].nurse_name

def test_login_name_success(nurse_service, anna):
    result = nurse_service.login(user_input=anna["nurse"].nurse_name, pw=anna["pw"])
    assert result.nurse_id == anna["nurse"].nurse_id
    assert result.nurse_name == anna["nurse"].nurse_name

def test_login_if_wrong_pw(nurse_service, anna):
    wrong_pw_result = nurse_service.login(user_input=anna["nurse"].nurse_name, pw=(anna["pw"]+"1"))
    assert wrong_pw_result is None

def test_login_if_wrong_name(nurse_service, anna):
    wrong_name_result = nurse_service.login(user_input=(anna["nurse"].nurse_name+"x"), pw=(anna["pw"]))
    assert wrong_name_result is None


def test_registration_success(anna):
    assert anna["name"] == anna["nurse"].nurse_name
    assert isinstance(anna["nurse"].nurse_id, int)

def test_registration_fails_if_name_exists(nurse_service, anna):
    repeat_anna = nurse_service.registration(nurse_name=anna["nurse"].nurse_name, pw=anna["pw"])
    assert repeat_anna is None

def test_registration_if_name_invalid(nurse_service):
    result = nurse_service.registration(nurse_name="anna", pw="test1234")
    assert result is None

def test_registration_if_pw_invalid(nurse_service):
    result = nurse_service.registration(nurse_name="Anna Schmidt", pw="invalid")
    assert result is None


def test_whitespaces(nurse_service):
    name = " Anna Schmidt "; pw="test1234"
    result_1 = nurse_service.registration(nurse_name=name, pw=pw)
    result_2 = nurse_service.login(user_input=name, pw=pw)
    assert result_1.nurse_name == name.strip()
    assert result_2.nurse_name == name.strip()


def test_val_name_limits(nurse_service):
    result_1 = nurse_service.val_name(search_value="Anna")
    result_2 = nurse_service.val_name(search_value="A Test")
    result_3 = nurse_service.val_name(search_value="Test B")
    result_4 = nurse_service.val_name(search_value="")
    result_5 = nurse_service.val_name(search_value="Te st")
    result_6 = nurse_service.val_name(search_value="longestnameeverr longestnameeverr")
    result_7 = nurse_service.val_name(search_value="  Anna with Blankspaces  ")
    result_8 = nurse_service.val_name(search_value=" Anna Blank ")
    assert result_1 is False and result_2 is False and result_3 is False
    assert result_4 is False and result_5 is True and result_6 is True
    assert result_7 is False and result_8 is True


def test_val_pw_limits(nurse_service):
    result_1 = nurse_service.val_pw(pw="only6LL")
    result_2 = nurse_service.val_pw(pw="1234Ihave33letters921234567893123")
    result_3 = nurse_service.val_pw(pw="")
    result_4 = nurse_service.val_pw(pw="eightcor")
    result_5 = nurse_service.val_pw(pw="32arecorrecthere5678921234567893")
    result_6 = nurse_service.val_pw(pw="do i take blank spaces")
    assert result_1 is False and result_2 is False and result_3 is False
    assert result_4 is True and result_5 is True and result_6 is True


def test_double_hash_pw(nurse_service):
    result_1 = nurse_service.hash_pw(pw="test1234")
    result_2 = nurse_service.hash_pw(pw="test1234")
    bool_1 = nurse_service.ver_pw(pw="test1234", hashed_pw=result_1)
    bool_2 = nurse_service.ver_pw(pw="test1234", hashed_pw=result_2)
    bool_3 = nurse_service.ver_pw(pw="test1134", hashed_pw=result_1)
    bool_4 = nurse_service.ver_pw(pw="test1224", hashed_pw=result_2)
    assert result_1 != result_2
    assert bool_1 is True and bool_2 is True
    assert bool_3 is False and bool_4 is False
