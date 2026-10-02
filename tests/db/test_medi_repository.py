def test_search_by_input(medi_repository, db):
    db.execute("""
               INSERT INTO medications (ingredient, df, strength, route, trade_name)
               VALUES
               ('medi_1', 'df_1', 'strength_1', 'route_1', 'trade_name_1'),
               ('medi_2', 'df_2', 'strength_2', 'route_2', 'trade_name_2'),
               ('medi_3', 'df_3', 'strength_3', 'route_3', 'trade_name_3'),
               ('drug_4', 'df_4', 'strength_4', 'route_4', 'trade_name_4'),
               ('drug_5', 'df_5', 'strength_5', 'route_5', 'trade_name_5')
               """)
    user_input = "medi"
    result = medi_repository.search_by_input(user_input=user_input)
    assert len(result) == 3

def test_search_input_is_None(medi_repository, db):
    db.execute("""
               INSERT INTO medications (ingredient, df, strength, route, trade_name)
               VALUES
               ('medi_1', 'df_1', 'strength_1', 'route_1', 'trade_name_1'),
               ('medi_2', 'df_2', 'strength_2', 'route_2', 'trade_name_2'),
               ('medi_3', 'df_3', 'strength_3', 'route_3', 'trade_name_3'),
               ('drug_4', 'df_4', 'strength_4', 'route_4', 'trade_name_4'),
               ('drug_5', 'df_5', 'strength_5', 'route_5', 'trade_name_5')
               """)
    user_input = "false"
    result = medi_repository.search_by_input(user_input=user_input)
    assert isinstance(result, list)
    assert len(result) == 0

def test_get_strengths(medi_repository, db):
    db.execute("""
               INSERT INTO medications (ingredient, strength)
               VALUES
               ('medi_1', 'strength_1'),
               ('medi_1', 'strength_2'),
               ('medi_2', 'strength_3'),
               ('medi_1', 'strength_1')
               """)
    chosen_ingredient = "medi_1"
    result = medi_repository.get_strengths(chosen_ingredient=chosen_ingredient)
    strengths = [row["strength"] for row in result]
    assert strengths == ["strength_1", "strength_2", "strength_1"]


def test_get_strengths_is_none(medi_repository, db):
    db.execute("""
               INSERT INTO medications (ingredient, strength)
               VALUES
               ('medi_1', 'strength_1'),
               ('medi_1', 'strength_2'),
               ('medi_2', 'strength_3'),
               ('medi_1', 'strength_1')
               """)
    chosen_ingredient = "false"
    result = medi_repository.get_strengths(chosen_ingredient=chosen_ingredient)
    assert isinstance(result, list)
    assert len(result) == 0

def test_search_df(medi_repository, db):
    db.execute("""
               INSERT INTO medications (ingredient, strength, df)
               VALUES
               ('medi_1', 'strength_1', 'df_1'),
               ('medi_1', 'strength_1', 'df_2'),
               ('medi_1', 'strength_1', 'df_3'),
               ('medi_1', 'strength_2', 'df_4'),
               ('medi_2', 'strength_1', 'df_5')
               """)
    chosen_ingredient = "medi_1"
    strength = "strength_1"
    result = medi_repository.search_df(chosen_ingredient=chosen_ingredient, strength=strength)
    dfs = [row["df"] for row in result]
    assert dfs == ["df_1", "df_2", "df_3"]

def test_search_df_is_none(medi_repository, db):
    db.execute("""
               INSERT INTO medications (ingredient, strength, df)
               VALUES
               ('medi_1', 'strength_1', 'df_1'),
               ('medi_1', 'strength_1', 'df_2'),
               ('medi_1', 'strength_1', 'df_3'),
               ('medi_1', 'strength_2', 'df_4'),
               ('medi_2', 'strength_1', 'df_5')
               """)
    chosen_ingredient = "false"
    strength = "false"
    result = medi_repository.search_df(chosen_ingredient=chosen_ingredient, strength=strength)
    assert isinstance(result, list)
    assert len(result) == 0
