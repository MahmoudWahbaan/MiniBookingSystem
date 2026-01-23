from src.Core.DB.DataBaseConnection import *
import datetime
class TimeSlot:
    def __init__(self, Client_ID=None, Host_ID, State='Free', StartTime, EndTime, BookedAt=None):
        self.__Client_ID = Client_ID
        self.__Host_ID = Host_ID
        self.__State = State
        self.__StartTime = StartTime
        self.__EndTime = EndTime
        self.__BookedAt = BookedAt