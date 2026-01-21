from Core.Modules.User import *
user = User("test@gmail.com", "test", "test", "test", "test", "test")
Done = user.InsertUser()
if Done:
    print("User Inserted Successfully")
else:
    print("User Insertion Failed")