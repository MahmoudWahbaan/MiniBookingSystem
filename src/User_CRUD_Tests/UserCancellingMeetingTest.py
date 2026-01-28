from src.Core.Modules.User import *
from src.Core.Modules.TimeSlot import *
from src.Core.Modules.Meeting import *

def ClearDB(username):
    if(User.SearchUser(username)):
        User.DeleteByUserName(username)


def Test():
    ClearDB("Host2")
    ClearDB("Client2")
    
    user1 = User("Host2", "Host2", "1234", "John", "Doe", "3435354")
    user1.InsertUser()
    user2 = User("Client2", "Client2", "1234", "Jane", "Doe", "1335345")
    user2.InsertUser()

    user1.CreateTimeSlot("2026:01:29:10:00", "2026:01:29:11:00")
    freeslotid = TimeSlot.FindFreeTimeSlotsForUser(user1.getUser_ID())
    if freeslotid and len(freeslotid) > 0:
        if user2.BookTimeSlot(freeslotid[0]):
            if Meeting.CancelMeeting(freeslotid[0]):
                print("Meeting cancelled successfully")
            else:
                print("Meeting cancellation failed")
        else:
            print("Booking failed") 
    else:
        print("No free time slots found")
    ClearDB("Host2")
    ClearDB("Client2")

Test()