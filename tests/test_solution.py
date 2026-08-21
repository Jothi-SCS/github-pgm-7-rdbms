import sqlite3
import os

DB_FILE = "marksheet.db"
SQL_FILE = "solution.sql"


def run_sql_file():
    """Execute the student's SQL file."""
    if not os.path.exists(SQL_FILE):
        raise AssertionError("solution.sql file not found.")

    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    conn = sqlite3.connect(DB_FILE)

    try:
        with open(SQL_FILE, "r", encoding="utf-8") as file:
            sql_script = file.read()

        conn.executescript(sql_script)
        conn.commit()
    except Exception as e:
        conn.close()
        raise AssertionError(f"SQL execution failed: {e}")

    return conn


def test_table_exists():
    """Test whether the Marksheet table exists."""
    conn = run_sql_file()

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
    """Test the structure of the Marksheet table."""
    conn = run_sql_file()

    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(Marksheet)")
    columns = cursor.fetchall()

    conn.close()

    column_names = [column[1] for column in columns]

    expected_columns = [
        "RollNo",
        "Name",
        "Department",
        "Marks"
    ]

    assert column_names == expected_columns, (
        f"Expected columns {expected_columns}, "
        f"but found {column_names}"
    )


def test_sample_data():
    """Test whether all five sample records are inserted."""
    conn = run_sql_file()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Marksheet")
    rows = cursor.fetchall()

    conn.close()

    expected_rows = [
        (1, "Arun", "CSE", 85),
        (2, "Divya", "IT", 78),
        (3, "Karthik", "CSE", 92),
        (4, "Nisha", "ECE", 67),
        (5, "Rahul", "IT", 88)
    ]

    assert rows == expected_rows, (
        f"Sample data is incorrect.\n"
        f"Expected: {expected_rows}\n"
        f"Found: {rows}"
    )


def test_marks_greater_than_80():
    """Test whether only students with marks greater than 80 are selected."""
    conn = run_sql_file()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT RollNo, Name, Department, Marks
        FROM Marksheet
        WHERE Marks > 80
        ORDER BY Marks DESC
    """)

    result = cursor.fetchall()

    conn.close()

    expected_result = [
        (3, "Karthik", "CSE", 92),
        (5, "Rahul", "IT", 88),
        (1, "Arun", "CSE", 85)
    ]

    assert result == expected_result, (
        f"Incorrect result.\n"
        f"Expected: {expected_result}\n"
        f"Found: {result}"
    )


def test_descending_order():
    """Test whether qualifying students are sorted by Marks descending."""
    conn = run_sql_file()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT Marks
        FROM Marksheet
        WHERE Marks > 80
        ORDER BY Marks DESC
    """)

    marks = [row[0] for row in cursor.fetchall()]

    conn.close()

    assert marks == sorted(marks, reverse=True), (
        "The result is not sorted in descending order of Marks."
    )


def test_no_student_below_or_equal_to_80():
    """Test that students with marks 80 or below are excluded."""
    conn = run_sql_file()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT RollNo, Name, Department, Marks
        FROM Marksheet
        WHERE Marks > 80
    """)

    result = cursor.fetchall()

    conn.close()

    for row in result:
        assert row[3] > 80, (
            f"Student with marks <= 80 found in result: {row}"
        )
