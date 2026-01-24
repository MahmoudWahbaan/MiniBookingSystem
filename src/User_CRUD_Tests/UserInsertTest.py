from src.Core.Modules.User import *
user = User("f@gmail.com", "f", "f", "f", "f", "f")
Done = user.InsertUser()
if Done:
    print("User Inserted Successfully")
    print(user.getUser_ID())
else:
    print("User Insertion Failed")
