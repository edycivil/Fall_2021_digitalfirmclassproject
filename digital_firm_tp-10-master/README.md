# Foreword
In this TP, we are putting it all together : Python, SQL & API's. The mechanisms are illustrated based on a simple example including students, courses and exams.
# Description
A university has multiple students, and multiple courses. Students are able to register to courses. Once they are registered, they are enrolled automatically to exams. Exams belong to sessions. Of course, students can fail exams, so they should be able to pass multiple exams for the same course.
To confirm their attendance to the exams, students make an API call with a secret only them know.
Teachers can then add the grade by doing an API call as well.
Finally, teachers should be able to list the results of a specific session, including the maximum grade, the minimum and the average one.
# Files Organisation
You can create your database running the `database_creation.py`
You can populate your database running the `database_population.py`
You can then run your app by running `main.py`
You can interact with the API using the `http-requests.http` file
