from src.Core.Modules.User import User
user = User("test@gmail.com", "test", "test", "test", "test", "test")
if user.DeleteUser("test"):
    print("User deleted successfully")
else:
    print("User not deleted")