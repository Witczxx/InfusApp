import sqlite3

class MediDb:
    def __init__(self, filepath, database):
        self.filepath = filepath
        self.con = sqlite3.connect(database)
        self.cur = self.con.cursor()
        self.raw_data = None
        self.sql_data = None

    ### NEW DATABASE / OVERWRITE EXISTING
    def create_database(self):
        self.raw_data = self.load_data()
        self.sql_data = self.format_data(raw_data=self.raw_data)
        self.create_table()
        self.add_columns(sql_data=self.sql_data)

    ### CLOSE & SAVE DATABASE
    def close_database(self):
        self.con.commit()
        self.con.close()

    ### LOAD DATA
    def load_data(self):
        with open(self.filepath, "r") as file:
            raw_data = file.readlines()
        return raw_data

    ### CONVERT .TXT INTO SQLITE FORMAT
    def format_data(self, raw_data):
        sql_data = []
        # Remove \n at line-ending
        for data in raw_data[1:]:
            # Remove Combination Preparations | Discontinued/Withdrawn Medications
            if data.count(";") == 1 and data.count("*") == 0:
                # Comma btw Day andYear
                data = data.replace(", ", " | ")
                # Comma in Strengths
                data = data.replace(",", "")
                # Exchanging Separator
                data = data.replace("~", ",")
                # Replace ';' btw DL and Route
                data = data.replace(";", ",")
                # Remove "\' (fill out where it appears)
                data = data.replace("\\", "/")
                # Add Line as Tuple to List
                sql_data.append(
                    tuple(data[:-1].split(",")),
                )
        return sql_data

    ### CREATE TABLE 'medications'
    def create_table(self):
        # If Previous FileExists
        self.cur.execute("DROP TABLE IF EXISTS medications")
        # Create Table Command
        self.cur.execute("""
            CREATE TABLE medications(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ingredient TEXT,
                df TEXT,
                route TEXT,
                trade_name TEXT,
                applicant TEXT,
                strength TEXT,
                appl_type TEXT,
                appl_no TEXT,
                product_no TEXT,
                te_code TEXT,
                approval_date TEXT,
                rld TEXT,
                rs TEXT,
                type TEXT,
                applicant_full_name TEXT
            )
        """)


