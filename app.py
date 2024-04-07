import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

db_config = {
    'dbname': 'finalassignment',
    'user': 'TA',
    'password': 'TA2024',
    'host': 'localhost'
}

def loadDDL(db_config):
    
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    
    try:
        with open('DDL.sql', 'r') as file:
            sql_script = file.read()
        
        cursor.execute(sql_script)
        conn.commit()
    except Exception as e:
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
        
def dropAllTables(db_config):
    
    conn = psycopg2.connect(**db_config)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            DROP TABLE IF EXISTS activity, admin, equipment, exercise, exerciseroutine,
            member, room, session, trainer, traineravailable, SessionMemberTable CASCADE;
        """)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        cursor.close()
        conn.close()

def loadDML(db_config):
    
    conn = psycopg2.connect(**db_config)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  
    cursor = conn.cursor()

    try:
        with open('DML.sql', 'r') as file:
            sql_script = file.read()

        cursor.execute(sql_script)
        conn.commit() 

    except Exception as e:
        conn.rollback()
        print(f"An error occurred while executing the DML script: {e}")

    finally:
        cursor.close()
        conn.close()

def connect_to_db():
    try:
        conn = psycopg2.connect(**db_config)
        return conn
    
    except Exception as e:
        print(f"Unable to connect to the database: {e}")
        return None

def run_sql_file(filename, connection):
    with open(filename, 'r') as sql_file:
        sql_script = sql_file.read()
    
    cur = connection.cursor()
    cur.execute(sql_script)
    cur.close()
    connection.commit()

def check_user_id(user_id):
    conn = connect_to_db()
    if conn is not None:
        cur = conn.cursor()
        
        try:
            cur.execute(sql.SQL("SELECT * FROM Admin WHERE adminID = %s"), (user_id,))
            if cur.fetchone():
                return "Admin"
            
            cur.execute(sql.SQL("SELECT * FROM Trainer WHERE trainerID = %s"), (user_id,))
            if cur.fetchone():
                return "Trainer"
            
            cur.execute(sql.SQL("SELECT * FROM Member WHERE memID = %s"), (user_id,))
            if cur.fetchone():
                return "Member"
            
        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            cur.close()
            conn.close()
    
    return None

def register_member():
    conn = connect_to_db()
    if conn is not None:
        try:
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            age = input("Enter your age: ")
            goal = input("Enter your fitness goal: ")
            weight = input("Enter your weight in kg: ")
            height = input("Enter your height in cm: ")
            billingType = input("Enter your billing type (e.g., monthly, annually): ")
            monthlyBill = 50

            cur = conn.cursor()
            
            cur.execute(sql.SQL("""
                INSERT INTO Member (name, email, age, goal, weight, height, billingType, monthlyBill)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING memID;
                """), (name, email, int(age), goal, int(weight), int(height), billingType, int(monthlyBill)))

            user_id = cur.fetchone()[0]
            conn.commit()
            print(f"Registration successful. Your Member ID is {user_id}.")
            memberDashboard(user_id)
        except Exception as e:
            print(f"An error occurred during registration: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

def adminDashboard(admin_id):
    while True:
        print("\n--- Admin Dashboard ---")
        print("1. Room Booking Management")
        print("2. Equipment Maintenance Monitoring")
        print("3. Class Schedule Updating")
        print("4. Billing and Payment Processing")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        conn = connect_to_db()
        cur = conn.cursor()

        if choice == '1':
            print("Managing Room Bookings...")
            showRoomsAndSessions()
        elif choice == '2':
            print("Monitoring Equipment Maintenance...")
            cur.execute("SELECT * FROM Equipment")
            equipment = cur.fetchall()
            for item in equipment:
                print(f"Equipment ID: {item[0]}, Equipment Name: {item[1]}, Last Checked: {item[2]}, Next Check: {item[3]}")
        elif choice == '3':
            updateSessionTimeAndRoom()
        
        elif choice == '4':
            viewAndUpdateMemberBilling()
        elif choice == '5':
            print("Exiting Admin Dashboard...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

def updateSessionTimeAndRoom():
    conn = connect_to_db()  
    cur = conn.cursor()

    cur.execute("SELECT sesID, sesName FROM Session")
    sessions = cur.fetchall()
    print("\nAvailable Sessions:")
   
    for session in sessions:
        print(f"Session ID: {session[0]}, Session Name: {session[1]}")
    
    sesID = input("Enter Session ID to update (or type 'exit' to cancel): ")
    
    if sesID.lower() == 'exit':
        return

    cur.execute("""
    SELECT trainerAvaID, trainerID, days, time 
    FROM TrainerAvailable 
    WHERE trainerAvaID NOT IN (SELECT trainerAvaID FROM Session WHERE sesID = %s)
    """, (sesID,))
    availableTimes = cur.fetchall()
    
    print("\nAvailable Times from Trainers:")
    
    for time in availableTimes:
        print(f"Trainer Available ID: {time[0]}, Trainer ID: {time[1]}, Days: {time[2]}, Time: {time[3]}")
    trainerAvaID = input("Enter Trainer Available ID for the new time (or type 'exit' to cancel): ")
    
    if trainerAvaID.lower() == 'exit':
        return

    cur.execute("SELECT roomID, Name FROM Room")
    rooms = cur.fetchall()
    
    print("\nAvailable Rooms:")
    
    for room in rooms:
        print(f"Room ID: {room[0]}, Name: {room[1]}")
    
    roomID = input("Enter Room ID for the session (or type 'exit' to cancel): ")
    
    if roomID.lower() == 'exit':
        return

    cur.execute("""
    UPDATE Session 
    SET trainerAvaID = %s, roomID = %s 
    WHERE sesID = %s
    """, (trainerAvaID, roomID, sesID))
    
    conn.commit()
    
    print("Session updated successfully.")

def showRoomsAndSessions():
    query = """
    SELECT 
        r.roomID, 
        r.Name AS RoomName, 
        s.sesID, 
        s.sesName
    FROM 
        Room r
    LEFT JOIN 
        Session s ON r.roomID = s.roomID
    ORDER BY 
        r.roomID
    """

    con = connect_to_db()  
    curr = con.cursor()
    curr.execute(query)
    results = curr.fetchall()

    rooms = {} 

    for row in results:
        room_id, room_name, session_id, session_name = row
        if room_id not in rooms:
            rooms[room_id] = {"room_name": room_name, "sessions": []}
        if session_id:  
            rooms[room_id]["sessions"].append({"session_id": session_id, "session_name": session_name})

    for room_id, info in rooms.items():
        print(f"Room ID: {room_id}, Room Name: {info['room_name']}")
        if info["sessions"]:
            for session in info["sessions"]:
                print(f"  - Session ID: {session['session_id']}, Session Name: {session['session_name']}")
        else:
            print("  - No sessions scheduled")
        print()  

def update_personal_info(conn, memID):
    print("\n--- Update personal info ---")
    print("0. Exit")
    print("1. Name")
    print("2. Email")
    print("3. Age")
    print("4. Goal")
    print("5. Weight")
    print("6. Height")
    choice = input("Enter your choice (0-6): ")

    cursor = conn.cursor()

    if choice == "0":
        print("Exiting...")
        return
    
    elif choice == "1":
        new_name = input("Enter new name: ")
        cursor.execute("UPDATE Member SET name = %s WHERE memID = %s;", (new_name, memID))
        conn.commit()
        print("Name updated successfully!")

    elif choice == "2":
        new_email = input("Enter new email: ")
        cursor.execute("UPDATE Member SET email = %s WHERE memID = %s;", (new_email, memID))
        conn.commit()
        print("Email updated successfully!")

    elif choice == "3":
        new_age = int(input("Enter new age: "))
        cursor.execute("UPDATE Member SET age = %s WHERE memID = %s;", (new_age, memID))
        conn.commit()
        print("Age updated successfully!")

    elif choice == "4":
        new_goal = input("Enter new goal: ")
        cursor.execute("UPDATE Member SET goal = %s WHERE memID = %s;", (new_goal, memID))
        conn.commit()
        print("Goal updated successfully!")

    elif choice == "5":
        new_weight = int(input("Enter new weight: "))
        cursor.execute("UPDATE Member SET weight = %s WHERE memID = %s;", (new_weight, memID))
        conn.commit()
        print("Weight updated successfully!")

    elif choice == "6":
        new_height = input("Enter new height (in feet and inches): ")
        cursor.execute("UPDATE Member SET height = %s WHERE memID = %s;", (new_height, memID))
        conn.commit()
        print("Height updated successfully!")

    else:
        print("Invalid choice!")

    cursor.close()

def memberDashboard(member_id):
    print("\n--- Member Dashboard ---")
    print("0. Exit")
    print("1. View Exercise Routines")
    print("2. View Fitness Achievements")
    print("3. View Health Statistics")
    print("4. Update personal info")
    print("5. View participating sessions")
    choice = input("Enter your choice (0-5): ")

    while choice != "0":
      conn = connect_to_db()
      cur = conn.cursor()

      if choice == '1':
          # Assuming ExerciseRoutine table has memberID to relate routines to members
          cur.execute("SELECT * FROM Exercise WHERE routineID IN (SELECT routineID FROM Member WHERE memID = %s)", (member_id,))
          routines = cur.fetchall()
          cur.execute("SELECT ExerciseRoutine.Name FROM ExerciseRoutine WHERE routineID IN (SELECT routineID FROM Member WHERE memID = %s)", (member_id,))
          routineName = (cur.fetchall())
          try:
            exerciseList = routines[0][1].split(',')
            print(f"\n        --{routineName[0][0]}--")
            for i in range(len(exerciseList)):
              print(f"        {i}. {exerciseList[i]}")
          except:
              print("[ERROR] You are not enrolled in an exercise routine program.")
            
      elif choice == '2':
          print()
          cur.execute("SELECT goal FROM Member WHERE memID = %s", (member_id,))
          achievements = cur.fetchall()
          print(f"Your goal is to: {achievements[0][0]}")
      elif choice == '3':
          # Assuming health statistics are stored in the Member or a related table
          cur.execute(f"SELECT weight, height FROM Member WHERE memID = {member_id}")
          stats = cur.fetchone()
          print("\n      --HEALTH METRICS--")
          print(f"        Weight: {stats[0]}kg \n        Height: {stats[1]}cm")
      elif choice == '4':
            update_personal_info(conn, member_id)
      elif choice == '5':
          print("\n       Participating sessions:")
          joinedTable = viewJoinedSessions(member_id)
          if (len(joinedTable) == 0):
              print("       NONE...")
          else:
              for i in joinedTable:
                  print(f"       {i}")
          print("\nWould you like to \n 0. Exit \n 1. Join a session \n 2. Leave a session \n")
          sessionChoice = input("Enter Here: ")
          
          if sessionChoice == "1":
            joinSession(member_id, conn, cur)
          
          if sessionChoice == "2":
            leaveSession(member_id, conn, cur)
      else:
        print("Invalid choice.")
        
      print("\n--- Member Dashboard ---")
      print("0. Exit")
      print("1. View Exercise Routines")
      print("2. View Fitness Achievements")
      print("3. View Health Statistics")
      print("4. Update personal info")
      print("5. View participating sessions")
      choice = input("Enter your choice (0-5): ")

def leaveSession(memID, conn, curr):
    # Query to find all sessions the member is currently registered in
    curr.execute(f"SELECT Session.sesID, Session.sesName FROM Session INNER JOIN SessionMemberTable ON Session.sesID = SessionMemberTable.sesID WHERE SessionMemberTable.memID = {memID}")
    registered_sessions = curr.fetchall()

    if not registered_sessions:
        print("You are not registered in any sessions.")
        return
    
    print("\n        YOUR CURRENT SESSIONS\n")
    for session in registered_sessions:
        print(f"SESSION ID: {session[0]} NAME: {session[1]}")

    while True:
        idToLeave = input("Enter session ID to leave (-1 to exit): ")
        if idToLeave == "-1":
            return

        # Convert input to int and check if it's one of the session IDs
        try:
            idToLeave = int(idToLeave)
        except ValueError:
            print("Please enter a valid session ID.")
            continue

        if idToLeave not in [session[0] for session in registered_sessions]:
            print("Invalid session ID. Please try another.")
            continue
        
        # Check if the session exists and the member is enrolled
        curr.execute(f"SELECT * FROM SessionMemberTable WHERE sesID = {idToLeave} AND memID = {memID}")
        if curr.fetchone() is None:
            print("You are not enrolled in this session.")
            continue
        
        # If checks pass, remove member from session
        curr.execute(f"DELETE FROM SessionMemberTable WHERE sesID = {idToLeave} AND memID = {memID}")
        conn.commit()
        print("You have successfully left the session.")
        return

def viewJoinedSessions(memID):
    query = """
    SELECT 
        s.sesID, 
        s.sesName, 
        s.capacity,
        r.Name AS RoomName,
        ta.days AS AvailableDays,
        ta.time AS AvailableTime
    FROM 
        Session s
    JOIN 
        SessionMemberTable smt ON s.sesID = smt.sesID
    JOIN
        Room r ON s.roomID = r.roomID
    JOIN
        TrainerAvailable ta ON s.trainerAvaID = ta.trainerAvaID
    WHERE 
        smt.memID = {}
    """.format(memID)
  
    con = connect_to_db()
    curr = con.cursor()
    curr.execute(query)
    table = curr.fetchall()
    tableToSend = []
    for row in table:
        # Directly use the fetched data without extra queries
        session_id, session_name, capacity, room_name, available_days, available_time = row
        # if check_session_capacity(session_id):  # Ensure this check is correctly applied
        #     continue
        session_info = f"SESSION ID: {session_id} NAME: {session_name} CLASS SIZE: {capacity} ON {available_days} AT {room_name} during {available_time}"
        tableToSend.append(session_info)
    return tableToSend

def joinSession(memID, conn, curr):
    curr.execute("SELECT * FROM Session")
    print("\n        ALL AVAILABLE SESSIONS\n")
    table = curr.fetchall()
    okSessionID = []
    filteredTable = []
    for i in range(len(table)):
        raw = table[i]
        if check_session_capacity(raw[0]):
            continue
        curr.execute(f"SELECT days FROM TrainerAvailable WHERE TrainerAvailable.trainerAvaID = {table[i][2]}")
        days = (curr.fetchall())[0][0]

        curr.execute(f"SELECT time FROM TrainerAvailable WHERE TrainerAvailable.trainerAvaID = {table[i][2]}")
        time = (curr.fetchall())[0][0]

        curr.execute(f"SELECT Name FROM Room WHERE Room.roomID = {table[i][3]}")
        room = (curr.fetchall())[0][0]
        okSessionID.append(raw[0])
        filteredTable.append(f"SESSION ID: {raw[0]} NAME: {raw[1]} CLASS SIZE: {raw[4]} ON {days} AT {room} during {time}")
    for i in filteredTable:
        print(i)
    
    while True:
        idToJoin = input("Enter session ID to join (-1 to exit): ")
        if idToJoin == "-1":
            return

        if int(idToJoin) not in okSessionID:
            print("Invalid session ID or session full. Please try another.")
            continue

        # Check if member is already in session
        curr.execute(f"SELECT * FROM SessionMemberTable WHERE sesID = {idToJoin} AND memID = {memID}")
        if curr.fetchone() is not None:
            print("You are already enrolled in this session.")
            continue
        
        # If checks pass, add member to session
        print("Joining session...")
        curr.execute(f"INSERT INTO SessionMemberTable (sesID, memID) VALUES ({idToJoin}, {memID})")
        conn.commit()
        print("You have successfully joined the session.")
        return

def check_session_capacity(session_id):
    conn = connect_to_db()  # Utilizes your existing database connection function
    if conn is not None:
        try:
            cur = conn.cursor()
            # SQL to check session capacity against member count
            sql = """
            SELECT s.capacity, COUNT(sm.memID) AS member_count
            FROM Session s
            JOIN SessionMemberTable sm ON s.sesID = sm.sesID
            WHERE s.sesID = %s
            GROUP BY s.capacity
            """
            cur.execute(sql, (session_id,))
            result = cur.fetchone()
            
            if result:
                capacity, member_count = result
                return member_count >= capacity
            else:
                # No members in the session or session ID not found
                return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        finally:
            cur.close()
            conn.close()
      
def trainerDashboard(trainer_id):
    while True:  # Keeps the dashboard in a loop
        print("\n--- Trainer Dashboard ---")
        print("0. Exit")
        print("1. Set Availability")
        print("2. View Member Profiles")
        choice = input("Enter your choice (0-2): ")

        conn = connect_to_db()  # Assumes this function exists and connects to your database
        cur = conn.cursor()

        if choice == '1':
            print("Setting Availability...")
            days = input("Enter available days (e.g., Mon, Wed): ")
            time = input("Enter available time (e.g., 9am - 5pm): ")

            # Assuming the TrainerAvailable table has been properly set up to allow updates
            cur.execute("UPDATE TrainerAvailable SET days = %s, time = %s WHERE trainerID = %s;", (days, time, trainer_id))
            conn.commit()
            print("Availability set successfully.")
        elif choice == '2':
            print("Viewing Member Profiles...")
            member_name = input("Enter Member's name to search or 'exit' to return: ")
            
            if member_name.lower() == 'exit':  # Allows exiting back to the dashboard
                continue  # Skips the rest of the loop and shows the dashboard again

            cur.execute("SELECT memID, name, email, age, goal, weight, height, routineID FROM Member WHERE name ILIKE %s", (f"%{member_name}%",))
            members = cur.fetchall()
            if not members:
                print("No members found with that name.")
            else:
                for member in members:
                    print(f"\nMember ID: {member[0]}")
                    print(f"Name: {member[1]}")
                    print(f"Email: {member[2]}")
                    print(f"Age: {member[3]}")
                    print(f"Goal: {member[4]}")
                    print(f"Weight: {member[5]}")
                    print(f"Height: {member[6]}")
                    print(f"Routine ID: {member[7]}")
        elif choice == '0':
            print("Exiting Trainer Dashboard...")
            break  # Exits the loop and ends the function
        else:
            print("Invalid choice. Please enter a number between 0 and 2.")
        
        cur.close()  # Close cursor
        conn.close()  # Close connection

def viewAndUpdateMemberBilling():
    def fetchMembers():
        # Fetches and displays members with their billing information
        cur.execute("SELECT memID, name, monthlyBill, billingType FROM Member")
        members = cur.fetchall()
        print("\nCurrent Members and Billing Details:")
        for member in members:
            print(f"Member ID: {member[0]}, Name: {member[1]}, Monthly Bill: ${member[2]}, Billing Type: {member[3]}")
        return members

    def updateBilling(memID):
        # Updates billing details for a specific member
        new_bill = input("Enter new monthly bill amount: ")
        new_payment_method = input("Enter new billing type (e.g., Credit Card, PayPal): ")
        cur.execute("UPDATE Member SET monthlyBill = %s, billingType = %s WHERE memID = %s", (new_bill, new_payment_method, memID))
        conn.commit()
        print("Billing details updated successfully.")

    conn = connect_to_db()  # Assumes this function returns a DB connection
    cur = conn.cursor()

    members = fetchMembers()
    while True:
        memID = input("\nEnter Member ID to update billing details (or type 'exit' to finish): ")
        if memID.lower() == 'exit':
            break
        memID = int(memID)  # Converting input to int for comparison
        # Check if the entered Member ID is valid
        if any(member[0] == memID for member in members):
            updateBilling(memID)
        else:
            print("Invalid Member ID. Please try again.")

    print("Exiting billing update module.")

def main():
    print("Welcome to DataGym! Would you like to ... \n 0. Exit \n 1. Sign in \n 2. Register\n") 
    while (True):
      action = input("Input: ")
      if (int(action) >= 0 and int(action) <= 2):
          break

    if action == "1":
        user_id = input("Enter your ID: ").strip()
        user_type = check_user_id(user_id)
        if user_type:
            print(f"Welcome, {user_type} : {user_id}!")

            if user_type == "Admin":
                adminDashboard(user_id)

            elif user_type == "Trainer":
                trainerDashboard(user_id)

            else:
                memberDashboard(user_id)

        else:
            print("ID not recognized. Please register if you are a new member.")
    elif action == "2":
        register_member()
    else:
        print("Goodbye!")

if __name__ == "__main__":
    # if you would load to insert the tables and data, uncomment these two lines
    # loadDDL(db_config)
    # loadDML(db_config)
    main()
    # if you would like to reset database on closure, uncomment this line.
    # dropAllTables(db_config)
