from src.Core.DB.DataBaseConnection import *
from src.Core.Utils.DateAndTime import *
from datetime import datetime
from src.Core.Modules.TimeSlot import *

class User:
    def __init__(self ,  __Email , __UserName , __Password , __FirstName , __LastName , __ContactNumber):
        self.__Email = __Email
        self.__UserName = __UserName
        self.__Password = __Password
        self.__FirstName = __FirstName
        self.__LastName = __LastName
        self.__ContactNumber = __ContactNumber
        self.__User_ID = None
    
    def __str__(self):
        return f"Email: {self.__Email}, UserName: {self.__UserName}, FirstName: {self.__FirstName}, LastName: {self.__LastName}, ContactNumber: {self.__ContactNumber}"

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
        self.__UpdateUser()
    
    def setEmail(self, __Email):
        self.__Email = __Email
        self.__UpdateUser()
    
    def setUserName(self, __UserName):
        self.__UserName = __UserName
        self.__UpdateUser()
    
    def setFirstName(self, __FirstName):
        self.__FirstName = __FirstName
        self.__UpdateUser()
    
    def setLastName(self, __LastName):
        self.__LastName = __LastName
        self.__UpdateUser()
    
    def setContactNumber(self, __ContactNumber):
        self.__ContactNumber = __ContactNumber
        self.__UpdateUser()
    
    def getUser_ID(self):
        if self.__User_ID is None:
            try :
                connection = connect()
                db_cursor = cursor(connection)
                query = "SELECT User_ID FROM User WHERE UserName = %s"
                values = (self.__UserName,)
                db_cursor.execute(query, values)
                self.__User_ID = db_cursor.fetchone()[0]
                db_cursor.close()
                connection.close()
                return self.__User_ID
            except Exception as e:
                print(e)
                return None
        return self.__User_ID
    
    def InsertUser(self):
        try:
            connection = connect()
            db_cursor = cursor(connection)
            query = "INSERT INTO User (Email, UserName, Password_Hash, FirstName, LastName, ContactNumber) VALUES (%s, %s, SHA2(%s, 256), %s, %s, %s)"
            values = (self.__Email, self.__UserName, self.__Password, self.__FirstName, self.__LastName, self.__ContactNumber)
            db_cursor.execute(query, values)
            self.__User_ID = db_cursor.lastrowid
            connection.commit()
            db_cursor.close()
            connection.close()
            return True
        except Exception as e:
            print(e)
            return False
    
    def DeleteUser(self):
        try:
            connection = connect()
            db_cursor = cursor(connection)
            query = "DELETE FROM User WHERE UserName = %s"
            values = (self.__UserName,)
            db_cursor.execute(query, values)
            connection.commit()
            db_cursor.close()
            connection.close()
            return True
        except Exception as e:
            print(e)
            return False
    
    @staticmethod
    def SearchUser(UserName):
        try:
            connection = connect()
            db_cursor = cursor(connection)
            query = "SELECT * FROM User WHERE UserName = %s"
            values = (UserName,)
            db_cursor.execute(query, values)
            result = db_cursor.fetchone()
            db_cursor.close()
            connection.close()
            if result is not None:
                return True
            return False
        except Exception as e:
            print(e)
            return None
    
    def __UpdateUser(self):
        try:
            connection = connect()
            db_cursor = cursor(connection)
            query = "UPDATE User SET Email = %s, Password_Hash = SHA2(%s, 256), FirstName = %s, LastName = %s, ContactNumber = %s WHERE UserName = %s"
            values = (self.__Email, self.__Password, self.__FirstName, self.__LastName, self.__ContactNumber, self.__UserName)
            db_cursor.execute(query, values)
            connection.commit()
            db_cursor.close()
            connection.close()
            return True
        except Exception as e:
            print(e)
            return False

    def CreateTimeSlot(self,StartTime,EndTime):
        try:
            if not validateDate(StartTime) or not validateDate(EndTime):
                print("Invalid Date")
                return False
            if(PrepareDate(StartTime) >= PrepareDate(EndTime)):
                print("Invalid Date")
                return False
            Host_ID = self.getUser_ID()
            State = 'Free'
            Slot = TimeSlot(Host_ID,State,PrepareDate(StartTime),PrepareDate(EndTime))
            return True
        except Exception as e:
            print(e)
            return False
    
    def BookTimeSlot(self, TimeSlot_ID):
        return TimeSlot.BookTimeSlot(TimeSlot_ID, self.getUser_ID())