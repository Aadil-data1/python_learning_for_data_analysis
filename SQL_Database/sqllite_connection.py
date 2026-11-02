import sqlite3           # SQLite is a relational database management system.
from pathlib import Path

DB_PATH = Path(__file__).with_name("company.db")

connection = sqlite3.connect(DB_PATH)    # The variable connection represents our active connection to the database

try:
    with connection:

        cursor = connection.cursor()   # cursor executes SQL statements through the connection

        # Create table                     # execute() sends an SQL command.
        cursor.execute("""                                
            CREATE TABLE IF NOT EXISTS Employees (  

                Employee_ID INTEGER PRIMARY KEY,
                Name TEXT NOT NULL,
                Department TEXT NOT NULL,
                Salary REAL NOT NULL CHECK(Salary >= 0)

            )
        """)

        # Sample employee records
        employees = [

            (101, "Aisha", "Engineering", 65000),
            (102, "Rahul", "HR", 48000),
            (103, "Meera", "Engineering", 72000),
            (104, "Kabir", "Finance", 58000),
            (105, "Sana", "HR", 52000)

        ]

        # Insert without duplicating existing employee IDs
        cursor.executemany("""
            INSERT OR IGNORE INTO Employees
            VALUES (?, ?, ?, ?)                
        """, employees)                  # question marks are placeholders.

        # Retrieve records
        cursor.execute("""
            SELECT *
            FROM Employees
            ORDER BY Employee_ID
        """)

        results = cursor.fetchall()

        for employee in results:
            print(employee)

finally:
    connection.close()