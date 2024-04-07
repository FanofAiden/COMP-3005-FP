<h1> Authors and Summary of Application.</h1>
Momo Radaideh 101292701<br>
Aiden Fan 101266368<br>
Final Project for COMP 3005: Health and Fitness Club Management System<br>

This is a Python program that interacts with a PostgreSQL server. It provides functionality for a simple Fitness club management system.<br>

<H1> Setup </H1>
- Have Python installed on machine.
- Run the following command in the shell of your choice and within the directory of this folder to install psycopg2
  `pip install psycopg2`

Instructions:<br>
If you choose to use your machine's cmd, run the following command to run the program: `app.py`<br>If you choose to run on an IDE like VSCode, just run it<br><br>
The program is connected to the specific database called `finalassignment`. The username is `postgres` and the password is `postgres`. The host is `localhost`  and the port is `5432` .<br>

Create the `finalassignment` database<br>
  This is done in the `DDL` sql file.<br>
  Input these commands into the SQL Shell (psql)<br>
  Make sure you're inside the `finalassignment` database<br>
    
<h2> IMPORTANT  NOTES FOR STARTUP</h2>

<p> You must go into the `db_config` dictionary object in the app.py file to modify the info to your liking. For example, if you have a custom pgadmin4 login (username and/or password) update with your personal info there. You must also have created the database called `finalassignment` before running application. </p>
  <br> Before running the program, in the main() function, there are some options to run this program.  Comment/Uncomment if youd like to ...<br>
  <br> 1. loadDDL() loads the DDL file. ONLY RUN THIS ON FIRST TIME BOOT, OR ELSE YOU WILL FACE ERRORS IF YOU DO NOT DROP TABLES AFTER. <br>
  <br> 2. loadDML() loads the DML File. ONLY RUN THIS FILE ON FIRST BOOT OR ELSE YOU WILL FACE ERRORS. This is sample data for the database <br>
  <br> 3. dropAllTables() drops a;ll tables. If you want to reset database after closing app, leave uncommenetd. with this uncommneted you can pair with previous two functions so every boot is a fresh wipe of newly added     data. <br>

<h1> Program Navigation </h1>
Once the program is running, you are given options to login, register, or exit:<br>
**ALL INPUTED DATA MUST BE WITHIN CONSTRAINTS**<br>

<br> Member Functions <br>
<br> Member's can register as a new member or sign in using their ID alone. They are able to view their signed up classes and classes to sign up as well as achievements in their fitness journey. They can see their on file Health Statistics and they are able to update personal info aswell. All avaiable classes are displayed to the member when they navigate through the menu and are prompted to enter the id of the course they would like to enroll in. <br>

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
