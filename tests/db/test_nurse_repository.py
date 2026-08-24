def test_nurse_repository_for_success(nurse_repository):
    nurse = nurse_repository.add_to_db(nurse_id=1234567, nurse_name="Anna", hash_pw="hashtest1234hash")
    result_1 = nurse_repository.search_by_input(user_input=nurse["nurse_id"])
    result_2 = nurse_repository.search_by_input(user_input=nurse["nurse_name"])
    assert result_1["nurse_id"] == result_2["nurse_id"] == nurse["nurse_id"]
    assert result_1["nurse_name"] == result_2["nurse_name"] == nurse["nurse_name"]

def test_nurse_repository_for_failure(nurse_repository):
    nurse = nurse_repository.add_to_db(nurse_id=1234567, nurse_name="Anna", hash_pw="hashtest1234hash")
    result = nurse_repository.search_by_input(user_input="Annna")
    assert result is None

def test_add_to_db_with_wrong_datatype(nurse_repository):
    nurse = nurse_repository.add_to_db(nurse_id="x", nurse_name="Anna", hash_pw="hashtest1234hash")
    assert nurse["nurse_id"] == "x" # SQLite documents wrong data types
