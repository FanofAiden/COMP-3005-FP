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

<br> Admin Function<br>
<br> Admin can manage room bookings for all sessions. Admin monitors equipment maintenance, meaning when equipment was last checked and when it should be checked next. Admin also updates class scheduling for both trainer and memebers as well as view billing and payment for members.

<br> Member Functions <br>
<br> Member's can register as a new member or sign in using their ID alone. They are able to view their signed up classes and classes to sign up as well as achievements in their fitness journey. They can see their on file Health Statistics and they are able to update personal info aswell. All avaiable classes are displayed to the member when they navigate through the menu and are prompted to enter the id of the course they would like to enroll in. <br>

<h1> Function Summaries. </h1>

`loadDDL(db_config)`: Connects to the database using provided configuration to execute DDL SQL script, creating or altering database schema.<br>

`dropAllTables(db_config)`: Drops specified tables from the database, allowing for a clean reset of the database schema.<br>

`loadDML(db_config)`: Loads initial data into the database by executing DML SQL commands from a file, populating tables with data.<br>

`connect_to_db()`: Establishes and returns a connection to the database using the global db_config dictionary.<br>

`run_sql_file(filename, connection)`: Executes SQL commands from a specified file using an established database connection, allowing for script-based database manipulation.<br>

`check_user_id(user_id)`: Queries the database to determine the type of user (Admin, Trainer, Member) based on the provided user ID and returns the user type.<br>

`register_member()`: Registers a new member in the database by collecting personal information and inserting it into the Member table.<br>

`adminDashboard(admin_id)`: Provides an admin user with an interactive dashboard to manage room bookings, equipment maintenance, class schedules, and billing.<br>

`updateSessionTimeAndRoom()`: Allows an admin to update the time and room assignment for an existing session, reflecting changes in schedule or location.<br>

`showRoomsAndSessions()`: Displays a list of rooms and their associated sessions, providing an overview of the schedule and availability.<br>

`update_personal_info(conn, memID)`: Offers a member the ability to update their personal information, including name, email, age, fitness goals, weight, and height.<br>

`memberDashboard(member_id)`: Provides a member with an interactive dashboard to view exercise routines, achievements, health stats, update info, and manage session participation.<br>

`leaveSession(memID, conn, curr)`: Enables a member to leave a session they are currently registered in, removing their participation from the session.<br>

`viewJoinedSessions(memID)`: Lists the sessions that a member has joined, providing details such as session ID, name, capacity, and timing.<br>

`joinSession(memID, conn, curr)`: Allows a member to join an available session, checking for session capacity and adding the member to the session if space is available.<br>

`check_session_capacity(session_id)`: Checks if a session has reached its capacity by comparing the number of registered members against the session's maximum capacity.<br>

`trainerDashboard(trainer_id)`: Provides trainers with an interactive dashboard to set their availability and view member profiles based on search criteria.<br>

`viewAndUpdateMemberBilling()`: Displays current members and their billing details, offering options to update billing amounts and methods for individual members.<br>

`main()`: Serves as the entry point for the script, providing users with options to sign in, register, or exit, and navigating to the appropriate functionality based on their choice.<br>


**NOT SHOWN/NEEDED IN VIDEO**<br>
when a user decides to exit, the `DROP TABLE students;` command runs and deletes the table. <br>

Video Demo:
https://youtu.be/GgFBXbvQFo4
