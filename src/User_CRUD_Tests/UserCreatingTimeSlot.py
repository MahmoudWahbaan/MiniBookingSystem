from src.Core.Modules.User import *
from src.Core.Modules.TimeSlot import *

# TEST 1 
user = User("TestTimeSlotInsert@gmail.com","TestTimeSlotInsert","TestTimeSlotInsert","TestTimeSlotInsert","TestTimeSlotInsert","TestTimeSlotInsert")
test1 = user.InsertUser()
if test1:
    print("User Inserted Successfully - TEST 1 Successed")
    print(user.getUser_ID())
else:
    print("User Insertion Failed - TEST 1 Failed")
# TEST 2
test2 = user.CreateTimeSlot("2022:01:01:00:00","2022:01:01:01:00")

if test2:
    print("Time Slot Created Successfully - TEST 2 Successed")
else:
    print("Time Slot Creation Failed - TEST 2 Failed")

# TEST 3
test3 = user.CreateTimeSlot("2033:01:01:29:00","2033:01:01:30:00")
if test3:
    print("Time Slot Created Successfully - TEST 3 Failed")
else:
    print("Time Slot Creation Failed - TEST 3 Successed")

# TEST 4
test4 = user.CreateTimeSlot("2022:01:01:02:00","2022:01:01:01:00")
if test4:
    print("Time Slot Created Successfully - TEST 4 Failed")
else:
    print("Time Slot Creation Failed - TEST 4 Successed")
