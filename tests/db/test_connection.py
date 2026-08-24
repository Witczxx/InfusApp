def test_fetchone(db):
    db.execute("""
               INSERT INTO nurses (nurse_id, nurse_name, hash_pw)
               VALUES (1000000, "Anna Schmidt", "test1234")
               """)
    result = db.fetchone("""
                SELECT nurse_id, nurse_name, hash_pw FROM nurses WHERE nurse_id = 1000000
                """)
    assert result["nurse_id"] == 1000000
    assert result["nurse_name"] == "Anna Schmidt"
    assert result["hash_pw"] == "test1234"


def test_fetchall(db):
    data = [
        (1000000, "Anna Schmidt", "test1234"),
        (1234567, "Max Mustermann", "12test34"),
        (8912345, "Peter Pan", "1234test"),
    ]
    db.executemany(
        ("""
            INSERT INTO nurses (nurse_id, nurse_name, hash_pw)
            VALUES (?, ?, ?)
             """),
        data,
    )
    results = db.fetch_all("""
                SELECT nurse_id, nurse_name, hash_pw FROM nurses
                """)
    assert data == [tuple(row) for row in results]
