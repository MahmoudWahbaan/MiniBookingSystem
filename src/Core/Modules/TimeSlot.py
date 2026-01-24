from src.Core.DB.DataBaseConnection import *
from src.Core.Modules.User import *
from src.Core.Utils.DateAndTime import *
import datetime
class TimeSlot:
    def __init__(self, Host_ID, State, StartTime, EndTime, BookedAt=None,Client_ID=None):
        self.__Client_ID = Client_ID
        self.__Host_ID = Host_ID
        self.__State = State
        self.__StartTime = StartTime
        self.__EndTime = EndTime
        self.__BookedAt = BookedAt
    
    def SetClientID(self, Client_ID):
        self.__Client_ID = Client_ID

    def SetHostID(self, Host_ID):
        self.__Host_ID = Host_ID
    
    def SetState(self, State):
        self.__State = State
    
    def SetStartTime(self, StartTime):
        self.__StartTime = StartTime
    
    def SetEndTime(self, EndTime):
        self.__EndTime = EndTime
    
    def SetBookedAt(self, BookedAt):
        self.__BookedAt = BookedAt

    def GetClientID(self):
        return self.__Client_ID
    
    def GetHostID(self):
        return self.__Host_ID
    
    def GetState(self):
        return self.__State
    
    def GetStartTime(self):
        return self.__StartTime
    
    def GetEndTime(self):
        return self.__EndTime
    
    def GetBookedAt(self):
        return self.__BookedAt
      
    def Insert(self):  
        try:
            connection = connect()
            db_cursor = cursor(connection)
            query = "INSERT INTO TimeSlot (Host_ID, State, StartTime, EndTime) VALUES (%s, %s, %s, %s)"
            db_cursor.execute(query, (self.__Host_ID, self.__State,self.__StartTime,self.__EndTime))
            connection.commit()
            db_cursor.close()
            connection.close()
            return True
        except Exception as e:
            print(e)
            return False
    
    @staticmethod
    def ShowAll():
        try:
            connection = connect()
            db_cursor = cursor(connection)
            query = "SELECT * FROM TimeSlot"
            db_cursor.execute(query)
            result = db_cursor.fetchall()
            db_cursor.close()
            connection.close()
            print(result)
            return True
        except Exception as e:
            print(e)
            return False