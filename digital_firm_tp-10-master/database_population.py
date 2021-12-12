import sqlite3

dbase = sqlite3.connect('tp10.db', isolation_level=None)
print('Database opened')
dbase.execute(''' 
                INSERT INTO Students
                (first_name , last_name, matricule, secret)
                VALUES ('Ernest', 'Solvay', 'ERNSOL01', '123456')
            ''')
dbase.execute(''' 
                INSERT INTO Teachers
                (first_name , last_name, secret)
                VALUES ('Chris', 'Castan', '123456')
            ''')
dbase.execute(''' 
                INSERT INTO Courses
                (name , teacher_id)
                VALUES ('Info', '1')
            ''')
dbase.execute(''' 
                INSERT INTO Sessions
                (course_id , session_date)
                VALUES ('1', '2021-12-19T01:00:00+01:00')
            ''')
dbase.close()
print('Database Closed')