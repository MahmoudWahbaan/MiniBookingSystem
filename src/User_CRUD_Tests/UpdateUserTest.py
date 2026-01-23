from src.Core.Modules.User import User
user = User("test@gmail.com", "test", "test", "test", "test", "test")
print(f"Before updating Username : {user}")
user.setUserName("test1")
print(f"After updating Username : {user}")
print(f"Found in DB after update : {User.SearchUser("test1")}")
