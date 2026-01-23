from src.Core.Modules.User import User
user = User("test@gmail.com", "test5", "test", "test", "test", "test")
if user.DeleteUser():
    print("User deleted successfully")
else:
    print("User not deleted")
print(f"Found in DB after delete : {User.SearchUser("test5")}")