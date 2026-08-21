import sqlite3
from pathlib import Path


STARTER_FILE = Path("starter.sql")
SOLUTION_FILE = Path("solution.sql")


def run_sql_files():
    conn = sqlite3.connect(":memory:")

    # First create the teacher's database/table/data
    starter_sql = STARTER_FILE.read_text()
    conn.executescript(starter_sql)

    return conn


def run_student_query(conn):
    solution_sql = SOLUTION_FILE.read_text().strip()

    # Execute student's SELECT query
    return conn.execute(solution_sql).fetchall()


def test_table_exists():
    conn = run_sql_files()

    cursor = conn.cursor()
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name='Marksheet'
    """)

    result = cursor.fetchone()
    conn.close()

    assert result is not None, "Marksheet table was not created."


def test_table_structure():
    conn = run_sql_files()

    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(Marksheet)")
    columns = cursor.fetchall()

    column_names = [column[1] for column in columns]

    expected_columns = [
        "RollNo",
        "Name",
        "Department",
        "Marks"
    ]

    conn.close()

    assert column_names == expected_columns, (
        f"Expected columns {expected_columns}, "
        f"but found {column_names}"
    )


def test_sample_data():
    conn = run_sql_files()

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Marksheet")
    rows = cursor.fetchall()

    conn.close()

    assert len(rows) == 5, (
        f"Expected 5 records, but found {len(rows)}"
    )


def test_marks_greater_than_80():
    conn = run_sql_files()

    rows = run_student_query(conn)

    expected = [
        (3, "Karthik", "CSE", 92),
        (5, "Rahul", "IT", 88),
        (1, "Arun", "CSE", 85)
    ]

    conn.close()

    assert rows == expected, (
        f"Expected {expected}, but found {rows}"
    )


def test_descending_order():
    conn = run_sql_files()

    rows = run_student_query(conn)

    marks = [row[3] for row in rows]

    conn.close()

    assert marks == sorted(marks, reverse=True), (
        "Students are not sorted by Marks in descending order."
    )


def test_no_student_below_or_equal_to_80():
    conn = run_sql_files()

    rows = run_student_query(conn)

    conn.close()

    assert all(row[3] > 80 for row in rows), (
        "Students with marks 80 or below were included."
    )
