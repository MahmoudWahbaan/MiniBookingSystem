from src.Core.Modules.User import *
from src.Core.Modules.TimeSlot import *

ExpectedVerdict = []
OutputVerdict = []

def ClearDataBase(username):
    try:
        connection = connect()
        db_cursor = cursor(connection)
        
        # Get User_ID first to delete related TimeSlots
        query_id = "SELECT ID FROM User WHERE UserName = %s"
        db_cursor.execute(query_id, (username,))
        result = db_cursor.fetchone()
        
        if result:
            user_id = result[0]
            # Delete Meetings related to TimeSlots of this user (if any)
            # This requires a more complex join delete or assuming cascade. 
            # For now, let's try deleting TimeSlots.
            query_ts = "DELETE FROM TimeSlot WHERE Host_ID = %s"
            db_cursor.execute(query_ts, (user_id,))
            
        # Now delete the user
        query = "DELETE FROM User WHERE UserName = %s"
        db_cursor.execute(query, (username,))
        
        connection.commit()
        db_cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(f"Error clearing database: {e}")
        return False

def Test():
    # TEST 1
    ClearDataBase("TestUser3")
    ClearDataBase("TestUser4") # Ensure clean state for both
    TestUser = User("TestUser3", "TestUser3", "TestUser3", "TestUser3", "TestUser3", "TestUser3")
    ExpectedVerdict.append(True)
    OutputVerdict.append(TestUser.InsertUser())
    
    # TEST 2
    ExpectedVerdict.append(False)
    OutputVerdict.append(TestUser.CreateTimeSlot("2020:01:02:12:00", "2020:01:01:12:00"))

    # TEST 3
    ExpectedVerdict.append(True)
    OutputVerdict.append(TestUser.CreateTimeSlot("2020:01:02:12:00", "2020:01:02:13:00"))

    # TEST 4
    ExpectedVerdict.append(True)
    TestUser2 = User("TestUser4", "TestUser4", "TestUser4", "TestUser4", "TestUser4", "TestUser4")
    OutputVerdict.append(TestUser2.InsertUser())

    # TEST 5
    ExpectedVerdict.append(False)
    User1_ID = TestUser.getUser_ID()
    User2_ID = TestUser2.getUser_ID()
    FreeTimeSlots = TimeSlot.FindFreeTimeSlotsForUser(User1_ID)
    print(f"TEST 5 PRE-OUTPUT: {FreeTimeSlots}")
    
    if FreeTimeSlots:
        # Try to book a non-existent slot ID (e.g. max_id + 100)
        # Using a large number to be safe, or just +1000 to the real ID
        OutputVerdict.append(TimeSlot.BookTimeSlot(FreeTimeSlots[0] + 9999, User2_ID))
    else:
        print("CRITICAL: No free time slots found for Test 5")
        OutputVerdict.append(True) # Force fail mistmatch

    # TEST 6
    ExpectedVerdict.append(True)
    if FreeTimeSlots:
         OutputVerdict.append(TimeSlot.BookTimeSlot(FreeTimeSlots[0], User2_ID))
    else:
         OutputVerdict.append(False)

    ClearDataBase("TestUser")
    ClearDataBase("TestUser2")

    for i in range(len(ExpectedVerdict)):
        result = "Passed" if ExpectedVerdict[i] == OutputVerdict[i] else f"Failed (Exp: {ExpectedVerdict[i]}, Got: {OutputVerdict[i]})"
        print(f"Test {i+1}: {result}")

Test()
