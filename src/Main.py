from src.Core.Modules.User import *
from src.Core.Modules.TimeSlot import *
from src.Core.Modules.Meeting import *
from src.Core.Utils.DateAndTime import validateDate, PrepareDate

def CreateFreeTimeSlot(UserName):
    print("\nDate format: YYYY:MM:DD:HH:MM (e.g., 2026:01:29:10:00)")
    StartTime = input("Enter Start Time: ")
    EndTime = input("Enter End Time: ")
    
    # Validate date format
    if not validateDate(StartTime) or not validateDate(EndTime):
        print("Invalid Date format")
        HomePage(UserName)
        return
    
    # Get Host_ID from UserName
    Host_ID = User.FindUserID(UserName)
    if Host_ID is None:
        print("User not found")
        HomePage(UserName)
        return
    
    # Create TimeSlot with correct parameters: Host_ID, State, StartTime, EndTime
    try:
        timeSlot = TimeSlot(Host_ID, 'Free', PrepareDate(StartTime), PrepareDate(EndTime))
        print("Time slot created successfully")
    except Exception as e:
        print(f"Time slot creation failed: {e}")
    HomePage(UserName)

def ShowAllFreeTimeSlots(UserName):
    print("\n--- All Time Slots ---")
    TimeSlot.ShowAll()
    HomePage(UserName)

def ShowAllFreeTimeSlotsForUser(UserName):
    print("\n--- Free Time Slots for User ---")
    TargetUserName = input("Enter UserName to search: ")
    result = TimeSlot.FindFreeTimeSlotsForUserByUserName(TargetUserName)
    if result:
        print(f"Free TimeSlot IDs: {result}")
    else:
        print("No free time slots found for this user")
    HomePage(UserName)

def BookMeetingByID(UserName):
    TimeSlotID = input("Enter TimeSlot ID to book: ")
    Client_ID = User.FindUserID(UserName)
    if Client_ID is None:
        print("User not found")
        HomePage(UserName)
        return
    
    Booked = TimeSlot.BookTimeSlot(TimeSlotID, Client_ID)
    if Booked:
        print("Meeting booked successfully")
    else:
        print("Meeting booking failed")
    HomePage(UserName)

def CancelMeetingByMeetingID(UserName):
    MeetingID = input("Enter Meeting ID to cancel: ")
    Cancelled = Meeting.CancelMeeting(MeetingID)
    if Cancelled:
        print("Meeting cancelled successfully")
    else:
        print("Meeting cancellation failed")
    HomePage(UserName)

def ShowAllMeetings(UserName):
    print("\n--- All Meetings ---")
    result = Meeting.ShowAllMeetings()
    if result:
        print(f"{'Meeting_ID':<12} {'State':<15} {'TimeSlot_ID':<12} {'StartTime':<20} {'EndTime':<20}")
        print("-" * 80)
        for row in result:
            Meeting_ID, State, TimeSlot_ID, StartTime, EndTime = row
            print(f"{Meeting_ID:<12} {State:<15} {TimeSlot_ID:<12} {str(StartTime):<20} {str(EndTime):<20}")
    else:
        print("No meetings found")
    HomePage(UserName)

def ShowAllMeetingsForUser(UserName):
    print("\n--- Meetings for User ---")
    TargetUserName = input("Enter UserName (Host) to search: ")
    Host_ID = User.FindUserID(TargetUserName)
    if Host_ID is None:
        print("User not found")
        HomePage(UserName)
        return
    
    result = Meeting.ShowAllMeetingsByHostID(Host_ID)
    if result:
        print(f"{'Meeting_ID':<12} {'State':<15} {'TimeSlot_ID':<12} {'StartTime':<20} {'EndTime':<20}")
        print("-" * 80)
        for row in result:
            Meeting_ID, State, TimeSlot_ID, StartTime, EndTime, Host_ID_val, Client_ID = row
            print(f"{Meeting_ID:<12} {State:<15} {TimeSlot_ID:<12} {str(StartTime):<20} {str(EndTime):<20}")
    else:
        print("No meetings found for this user")
    HomePage(UserName)

def HomePage(UserName):
    print(f"\n========================================")
    print(f"Home Page - Welcome {UserName}")
    print("========================================")
    print("Options:")
    print("1 - Create free time slot")
    print("2 - Show all time slots")
    print("3 - Show free time slots for user by UserName")
    print("4 - Book a meeting by TimeSlot ID")
    print("5 - Cancel Meeting by Meeting ID")
    print("6 - Show all meetings")
    print("7 - Show all meetings for user by UserName")
    print("8 - Logout")
    print("9 - Exit")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        CreateFreeTimeSlot(UserName)
    elif choice == "2":
        ShowAllFreeTimeSlots(UserName)
    elif choice == "3":
        ShowAllFreeTimeSlotsForUser(UserName)
    elif choice == "4":
        BookMeetingByID(UserName)
    elif choice == "5":
        CancelMeetingByMeetingID(UserName)
    elif choice == "6":
        ShowAllMeetings(UserName)
    elif choice == "7":
        ShowAllMeetingsForUser(UserName)
    elif choice == "8":
        print("Logging out...")
        LoginPage()
    elif choice == "9":
        print("Exiting...")
        exit()
    else:
        print("Invalid choice")
        HomePage(UserName)

def LoginPage():
    print("\n========================================")
    print("Mini Booking System - Login Page")
    print("========================================")
    print("1. Login")
    print("2. Register")
    print("3. Exit")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        UserName = input("Enter your UserName: ")
        Password = input("Enter your Password: ")
        if User.Login(UserName, Password):
            print("Login successful!")
            HomePage(UserName)
        else:
            print("Login failed - Invalid username or password")
            print("Redirecting to Login Page...")
            LoginPage()
    elif choice == "2":
        print("\n--- Registration ---")
        Email = input("Enter your Email: ")
        UserName = input("Enter your UserName: ")
        Password = input("Enter your Password: ")
        FirstName = input("Enter your FirstName: ")
        LastName = input("Enter your LastName: ")
        ContactNumber = input("Enter your ContactNumber: ")
        user = User(Email, UserName, Password, FirstName, LastName, ContactNumber)
        if user.InsertUser():
            print("User created successfully!")
            print("Redirecting to Login Page...")
            LoginPage()
        else:
            print("User creation failed")
            print("Redirecting to Login Page...")
            LoginPage()
    elif choice == "3":
        print("Exiting...")
        exit()
    else:
        print("Invalid choice")
        LoginPage()

if __name__ == "__main__":
    LoginPage()
