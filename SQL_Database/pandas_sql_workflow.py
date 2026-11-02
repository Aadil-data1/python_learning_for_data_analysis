import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DB_PATH = Path(__file__).with_name("company.db")

connection = sqlite3.connect(DB_PATH)

#try:

 #   query = """
  #      SELECT *
   #     FROM Employees
    #"""

    #df = pd.read_sql_query(query, connection)

    #print(df)

#finally:
 #   connection.close()

#print(df.head())
#print(df.info())
#print(df.describe())
#print(df.groupby("Department")["Salary"].mean())


# Departmental Salary Analysis
try:

    query = """
        SELECT

            Department,

            COUNT(*) AS Employee_Count,

            ROUND(AVG(Salary), 2) AS Average_Salary,

            MIN(Salary) AS Minimum_Salary,

            MAX(Salary) AS Maximum_Salary

        FROM Employees

        GROUP BY Department

        ORDER BY Average_Salary DESC
    """

    department_report = pd.read_sql_query(          # converting database information into pandas
        query,
        connection
    )

    print(department_report)

finally:
    connection.close()

# Visualise the departmental average salaries:

import matplotlib.pyplot as plt

plt.bar(
    department_report["Department"],
    department_report["Average_Salary"]
)

plt.xlabel("Department")
plt.ylabel("Average Salary")
plt.title("Average Salary by Department")

plt.show()

#Saving Pandas results back into a database

connection = sqlite3.connect(DB_PATH)

try:

    department_report.to_sql(
        "Department_Summary",
        connection,
        if_exists="replace",
        index=False
    )

finally:
    connection.close()