from pathlib import Path

from infusapp.db.connection import Database


def run(db: Database):
    create_table_nurses(db=db)
    create_table_patients(db=db)
    create_table_medications(db=db)
    create_table_infusions(db=db)


def create_table_nurses(db: Database) -> None:
    db.execute("DROP TABLE IF EXISTS nurses")
    db.execute("""
        CREATE TABLE nurses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nurse_id INT UNIQUE,
            nurse_name TEXT,
            hash_pw TXT
        )
    """)


def create_table_patients(db: Database) -> None:
    db.execute("DROP TABLE IF EXISTS patients")
    db.execute("""
        CREATE TABLE patients(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INT UNIQUE,
            patient_name TEXT
        )
    """)


def create_table_medications(db: Database) -> None:
    db.execute("DROP TABLE IF EXISTS medications")
    db.execute("""
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

def create_table_infusions(db: Database) -> None:
    db.execute("DROP TABLE IF EXISTS infusions")
    db.execute("""
        CREATE TABLE infusions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nurse_id INT UNIQUE,
            nurse_name TEXT,
            patient_id INT UNIQUE,
            patient_name TEXT,
            ingredient TEXT,
            strength TEXT,
            unit INT,
            dosage_form TEXT,
            carrier_fluid TEXT,
            total_volume INT,
            drops_per_min INT,
            ml_per_hour INT,
            start_time DATETIME,
            stop_time DATETIME
        )
    """)


if __name__ == "__main__":
    db_path: Path = Path(__file__).parent.parent / "data" / "infusapp.db"
    db: Database = Database(db_path=db_path)
    run(db=db)
    print("Table Creation Complete")
