from pathlib import Path

from infusapp.db.connection import Database


def run(txt_file: Path, db: Database) -> None:
    raw_data: list[str] = load_data(txt_file=txt_file)
    sql_data: list[tuple] = format_data(raw_data=raw_data)
    insert_medications(sql_data=sql_data, db=db)


def load_data(txt_file: Path) -> list[str]:
    with open(txt_file, "r") as file:
        raw_data: list[str] = file.readlines()
        return raw_data


def format_data(raw_data: list[str]) -> list[tuple]:
    sql_data: list[tuple] = []
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


def insert_medications(sql_data: list, db: Database) -> None:
    db.executemany(
        """
        INSERT INTO medications (
            ingredient,
            df,
            route,
            trade_name,
            applicant,
            strength,
            appl_type,
            appl_no,
            product_no,
            te_code,
            approval_date,
            rld,
            rs,
            type,
            applicant_full_name
        )
        VALUES(
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )""",
        sql_data,
    )


if __name__ == "__main__":
    txt_file: Path = Path(__file__).parent / "raw_data" / "medi_db.txt"
    db_path: Path = Path(__file__).parent.parent / "data" / "infusapp.db"
    db: Database = Database(db_path=db_path)
    run(txt_file=txt_file, db=db)
    print("Import Complete")

