import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).with_name("company.db")

connection = sqlite3.connect(DB_PATH)

# Enable foreign key enforcement in SQLite

connection.execute("PRAGMA foreign_keys = ON")

try:
    with connection:

        cursor = connection.cursor()

        # Create Departments table

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Departments (

                Department_ID INTEGER PRIMARY KEY,
                Department_Name TEXT NOT NULL UNIQUE

            )
        """)

        # Create Staff table

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Staff (

                Employee_ID INTEGER PRIMARY KEY,
                Name TEXT NOT NULL,
                Department_ID INTEGER NOT NULL,
                Salary REAL NOT NULL CHECK(Salary >= 0),

                FOREIGN KEY (Department_ID)
                REFERENCES Departments(Department_ID)

            )
        """)

        # Insert departments

        departments = [
            (1, "Engineering"),
            (2, "HR"),
            (3, "Finance"),
            (4, "Legal")
        ]

        cursor.executemany("""
            INSERT OR IGNORE INTO Departments
            VALUES (?, ?)
        """, departments)

        # Insert employees

        staff = [
            (201, "Sara", 1, 65000),
            (202, "Salman", 2, 48000),
            (203, "Fatima", 1, 72000),
            (204, "John", 3, 58000),
            (205, "Carey", 2, 52000)
        ]

        cursor.executemany("""
            INSERT OR IGNORE INTO Staff
            VALUES (?, ?, ?, ?)
        """, staff)

    print("Related tables created successfully!")

finally:
    connection.close()

# Executing the JOINS through Python and load it into Pandas

connection = sqlite3.connect(DB_PATH)

try:

    query = """
        SELECT
            s.Employee_ID,
            s.Name,
            d.Department_Name,
            s.Salary

        FROM Staff AS s

        INNER JOIN Departments AS d

        ON s.Department_ID = d.Department_ID

        ORDER BY s.Employee_ID
    """

    df = pd.read_sql_query(query, connection)

    print(df)

finally:
    connection.close()