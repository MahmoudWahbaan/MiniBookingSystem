from src.Core.DB.DataBaseConnection import *
class User:
    def __init__(self ,  __Email , __UserName , __Password , __FirstName , __LastName , __ContactNumber):
        self.__Email = __Email
        self.__UserName = __UserName
        self.__Password = __Password
        self.__FirstName = __FirstName
        self.__LastName = __LastName
        self.__ContactNumber = __ContactNumber
    
    def getUserName(self):
        return self.__UserName
    
    def getPassword(self):
        return self.__Password
    
    def getEmail(self):
        return self.__Email
    
    def getFirstName(self):
        return self.__FirstName
    
    def getLastName(self):
        return self.__LastName
    
    def getContactNumber(self):
        return self.__ContactNumber
    
    def setPassword(self, __Password):
        self.__Password = __Password
    
    def setEmail(self, __Email):
        self.__Email = __Email
    
    def setUserName(self, __UserName):
        self.__UserName = __UserName
    
    def setFirstName(self, __FirstName):
        self.__FirstName = __FirstName
    
    def setLastName(self, __LastName):
        self.__LastName = __LastName
    
    def setContactNumber(self, __ContactNumber):
        self.__ContactNumber = __ContactNumber
    
    def InsertUser(self):
        try:
            connection = connect()
            db_cursor = cursor(connection)
            query = "INSERT INTO User (Email, UserName, Password_Hash, FirstName, LastName, ContactNumber) VALUES (%s, %s, SHA2(%s, 256), %s, %s, %s)"
            values = (self.__Email, self.__UserName, self.__Password, self.__FirstName, self.__LastName, self.__ContactNumber)
            db_cursor.execute(query, values)
            connection.commit()
            db_cursor.close()
            connection.close()
            return True
        except Exception as e:
            print(e)
            return False
    
    def DeleteUser(self, UserName):
        try:
            connection = connect()
            db_cursor = cursor(connection)
            query = "DELETE FROM User WHERE UserName = %s"
            values = (UserName,)
            db_cursor.execute(query, values)
            connection.commit()
            db_cursor.close()
            connection.close()
            return True
        except Exception as e:
            print(e)
            return False