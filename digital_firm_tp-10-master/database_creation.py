import sqlite3

# We open a connection to the SQLite database file.
# If the given database name does not exist then this call will create the database.
# isolation_level=None -> Auto-commit
dbase = sqlite3.connect('tp10.db', isolation_level=None)
print('Database opened')

# Students
dbase.execute(''' CREATE TABLE IF NOT EXISTS Students (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    matricule TEXT NOT NULL,
    secret TEXT NOT NULL) ''')
print("Student table created successfully")

# Teachers
dbase.execute(''' CREATE TABLE IF NOT EXISTS Teachers (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    secret TEXT NOT NULL) ''')
print("Teacher table created successfully")

# Courses
dbase.execute(''' CREATE TABLE IF NOT EXISTS Courses (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    teacher_id INTEGER NOT NULL,
    FOREIGN KEY(teacher_id) REFERENCES Teachers(id)
    ) ''')
print("Courses table created successfully")

# Sessions
dbase.execute(''' CREATE TABLE IF NOT EXISTS Sessions (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    session_date DATE NOT NULL,
    FOREIGN KEY (course_id) REFERENCES Courses(id)
    ) ''')
print("Sessions table created successfully")

# Exams
dbase.execute(''' CREATE TABLE IF NOT EXISTS Exams (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    attendance BOOLEAN NULL,
    grade FLOAT,
    session_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    FOREIGN KEY (session_id) REFERENCES Sessions(id),
    FOREIGN KEY (student_id) REFERENCES Students (id)
    ) ''')
print("Students table created successfully")

dbase.close()
print('Database Closed')