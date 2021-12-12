import sqlite3

# We need to import the Request object as well:
from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.get("/")
def root():
  return {"message": "It works !"}

########################
# 1. Register a student
########################
@app.post("/register_student")
async def register_student(payload: Request):
    values_dict = await payload.json()
    # Open the DB
    dbase = sqlite3.connect('tp10.db', isolation_level=None)
    # Step 1: retrieve the session id

    query_session = dbase.execute(''' 
                    SELECT id FROM Sessions
                    WHERE course_id = {}               
                    '''.format(str(values_dict['course_id'])))
    # We then store the results of the query with fetchall.
    session_results = query_session.fetchall()[0][0]
    # Step 2: create a new exam for the student and session:
    query_exam = dbase.execute('''
            INSERT INTO Exams(student_id, session_id) 
            VALUES ({student}, {session})             
            '''.format(student=str(values_dict['student_id']), session=str(session_results)))
    # Close the DB
    dbase.close()
    return True

############################################
# 2. Confirm student attendance to an exam
############################################
@app.post("/confirm_attendance")
async def confirm_attendance(payload: Request):
  values_dict = await payload.json()
  # Open the DB
  dbase = sqlite3.connect('tp10.db', isolation_level=None, check_same_thread=False)

  # Step 1: retrieve the secret and id based on matricule

  secret_query = dbase.execute(''' 
                SELECT id, secret FROM Students
                WHERE id = {}
                '''.format(str(values_dict['student_id'])))

  secret = secret_query.fetchall()[0][1]

  # Step 2: check if secret is effectively equal:
  
  if secret != values_dict['secret']:
    return "error"
  exam = dbase.execute(''' 
                  UPDATE Exams
                  SET attendance = 1
                  WHERE session_id = {session_id}
                  AND student_id = {student_id}        
                  '''.format(session_id = values_dict['session_id'], student_id = values_dict['student_id']))
  # Close the DB
  dbase.close()
  return "Student {student_id} correcty registered to Session {session_id}".format(session_id = values_dict['session_id'], student_id = values_dict['student_id']) 

############################################
# 3. Grade an exam
############################################

@app.post("/grade_exam")
async def grade_exam(payload: Request):
  values_dict = await payload.json()
  # Open the DB
  dbase = sqlite3.connect('tp10.db', isolation_level=None, check_same_thread=False)

  # Step 1: retrieve the secret and id based on matricule

  secret_query = dbase.execute(''' 
                SELECT id, secret FROM Teachers
                WHERE id = {}
                '''.format(str(values_dict['teacher_id'])))

  secret = secret_query.fetchall()[0][1]

  # Step 2: check if secret is effectively equal:
  
  if secret != values_dict['secret']:
    return "error"
  exam = dbase.execute(''' 
                  UPDATE Exams
                  SET grade = {grade}
                  WHERE session_id = {session_id}
                  AND student_id = {student_id}        
                  '''.format(grade = values_dict['grade'], session_id = values_dict['session_id'], student_id = values_dict['student_id']))
  # Close the DB
  dbase.close()
  return True

############################################
# 4. Get all grades from a exam session
############################################

@app.get("/session_grades")
async def session_grades(payload: Request):
  values_dict = await payload.json()
  # Open the DB
  dbase = sqlite3.connect('tp10.db', isolation_level=None, check_same_thread=False)

  # Step 1: retrieve all the information about the session, underlying exams and students by joining the tables

  grades_query = dbase.execute(''' 
    SELECT Students.matricule, Exams.grade FROM Sessions
    LEFT JOIN Exams ON Exams.session_id = Sessions.id
    LEFT JOIN Students ON Exams.student_id = Students.id               
    WHERE Sessions.id  = {session_id}
    '''.format(session_id = str(values_dict['session_id'])))
  
  grades = grades_query.fetchall()

  # Step 2: clean the results

  # Close the DB
  dbase.close()
  return grades 

if __name__ == '__main__':
  uvicorn.run(app, host='127.0.0.1', port=8000)