from src.Core.Modules.User import User
user = User("test@gmail.com", "test", "test", "test", "test", "test")
user.InsertUser()
if user.SearchUser("test"):
    print("User found")
else:
    print("User not found")