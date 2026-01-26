from src.Core.DB.DataBaseConnection import *
from src.Core.Modules.User import *

class Authentication:
    def __init__():
        pass
    def Login(UserName , PassWord):
        try:
            connection = connect()
            db_cursor = cursor(connection)
            query = "SELECT * FROM User WHERE UserName = %s AND Password_Hash = SHA2(%s, 256)"
            values = (UserName, PassWord)
            db_cursor.execute(query, values)
            result = db_cursor.fetchone()
            db_cursor.close()
            connection.close()
            if result is not None:
                return True
            return False
        except Exception as e:
            print(e)
            return False
    def Register(Email, UserName, PassWord, FirstName, LastName, ContactNumber):
        if(User.SearchUser(UserName)):
            print("User Already Exists")
            return False
        new_user = User(Email, UserName, PassWord, FirstName, LastName, ContactNumber)
        return new_user.InsertUser()

    