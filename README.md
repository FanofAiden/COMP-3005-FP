Momo Radaideh 101292701<br>
Aiden Fan 101266368
Final Project for COMP 3005: Health and Fitness Club Management System

This is a Python program that interacts with a PostgreSQL server. It provides functionality for a simple Fitness club management system.

Setup:

- Have Python installed on machine.
- Run the following command in the shell of your choice and within the directory of this folder to install psycopg2
  `pip install psycopg2`

Instructions:<br>
If you choose to use your machine's cmd, run the following command to run the program: `app.py`<br>If you choose to run on an IDE like VSCode, just run it<br><br>
The program is connected to the specific database called `finalassignment`. The username is `postgres` and the password is `postgres`. The host is `localhost`  and the port is `5432` .<br>

Create the `finalassignment` database<br>
  This is done in the `DDL` sql file.<be>
  Input these commands into the SQL Shell (psql)<br>
    Make sure you're inside the `finalassignment` database<br>
    
Once you run the program, the tables are created and populated with inital data.<br>

Once the program is running, you are given options to login, register, or exit:<br>
**ALL INPUTED DATA MUST BE WITHIN CONSTRAINTS**<br>
If your input is:<br>
0. This exits the program<br>
1. This signs the user in by asking them to input a valid ID<br>
       The initial IDs are as follows:<br>
       Admin: 0<br>
       Mark, trainer: 100001<br>
       Nolan, trainer: 100002<br>
       Allen, trainer: 100003<br>
       Aiden, member: 1<br>
       Momo, member: 2<br>
       **ANY NEW MEMBER THAT GETS ADDED WILL START FROM 3 AND GO UP**<br>
       If user decides to log in as Admin:
             **You're taken to the admin dashboard, if you choose:**
             1. this allows admin to see available rooms
3. This calls the `register_member()` function where users can register and be created in the database


Documentation:<br>
`getAllStudents()` - function that retrieves and displays all records from the students table <br>
`addStudent(first_name, last_name, email, enrollment_date)` - inserts a new student record into the students table <br>
`updateStudentEmail(student_id, new_email)` - updates the email address for a student with the specified student_id <br>
`deleteStudent(student_id)` - deletes the record of the student with the specified student_id <br>
`main_menu()` - function that creates a menu for user input then calls corresponding functions until user chooses to exit<br>
`main()` - calls the `main_menu()` function<br>

**NOT SHOWN/NEEDED IN VIDEO**<br>
when a user decides to exit, the `DROP TABLE students;` command runs and deletes the table. <br>

Video Demo:
https://youtu.be/GgFBXbvQFo4
