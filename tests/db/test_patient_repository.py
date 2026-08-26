def test_patient_repository_for_success(patient_repository):
    patient = patient_repository.add_to_db(patient_id=1234567, patient_name="Max Mustermann")
    result_1 = patient_repository.search_by_input(user_input=patient["patient_id"])
    result_2 = patient_repository.search_by_input(user_input=patient["patient_name"])
    assert result_1["patient_id"] == result_2["patient_id"] == patient["patient_id"]
    assert result_1["patient_name"] == result_2["patient_name"] == patient["patient_name"]

def test_patient_repository_for_failure(patient_repository):
    patient = patient_repository.add_to_db(patient_id=1234567, patient_name="Max Mustermann")
    result = patient_repository.search_by_input(user_input="Maxx Mustermann")
    assert result is None

def test_add_to_db_with_wrong_datatype(patient_repository):
    patient = patient_repository.add_to_db(patient_id="x", patient_name="Max Mustermann")
    assert patient["patient_id"] == "x" # SQLite documents wrong data types
