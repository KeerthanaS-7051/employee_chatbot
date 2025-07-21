import sqlite3

conn = sqlite3.connect("employee.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS Employee")

cursor.execute("""
CREATE TABLE Employee (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    role TEXT,
    salary FLOAT,
    joining_date DATE
)
""")

cursor.executemany("""
INSERT INTO Employee (id, name, department, role, salary, joining_date)
VALUES (?, ?, ?, ?, ?, ?)
""", [
    (1, "Alice", "HR", "Manager", 70000.0, '2020-05-01'),
    (2, "Bob", "Engineering", "Developer", 85000.0, '2019-03-15'),
    (3, "Carol", "Finance", "Analyst", 60000.0, '2021-08-01'),
    (4, "David", "Engineering", "DevOps", 80000.0, '2022-01-10'),
    (5, "Eve", "HR", "Recruiter", 50000.0, '2023-02-20')
])

conn.commit()
conn.close()

print("employee.db created with new sample data.")