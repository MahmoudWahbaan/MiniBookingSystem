from src.Core.DB.DataBaseConnection import *
from src.Core.Modules.Meeting import *
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
        self.__TimeSlot_ID = None
        self.__Insert()
    
    def __SetClientID(self, Client_ID):
        self.__Client_ID = Client_ID
        try :
            Connection = connect()
            Cursor = cursor(Connection)
            Cursor.execute("UPDATE TimeSlot SET Client_ID = %s WHERE Host_ID = %s AND State = %s AND StartTime = %s AND EndTime = %s", (self.__Client_ID,self.__Host_ID,self.__State,self.__StartTime,self.__EndTime))
            Connection.commit()
            Cursor.close()
            Connection.close()
            return True
        except Exception as e:
            print(e)
            return False

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
    
    def __UpdateTimeSlot(self):
        try:
            Connection = connect()
            Cursor = cursor(Connection)
            Cursor.execute("UPDATE TimeSlot SET State = %s, StartTime = %s, EndTime = %s, BookedAt = %s WHERE Host_ID = %s AND State = %s AND StartTime = %s AND EndTime = %s", ( self.__State,self.__StartTime,self.__EndTime,self.__BookedAt,self.__Host_ID,self.__State,self.__StartTime,self.__EndTime))
            Connection.commit()
            Cursor.close()
            Connection.close()
            return True
        except Exception as e:
            print(e)
            return False

    
    def GetTimeSlotID(self):
        if self.__TimeSlot_ID is not None:
            return self.__TimeSlot_ID
        else:
            try :
                Connection = connect()
                Cursor = cursor(Connection)
                Cursor.execute("SELECT ID FROM TimeSlot WHERE Host_ID = %s AND State = %s AND StartTime = %s AND EndTime = %s", (self.__Host_ID, self.__State,self.__StartTime,self.__EndTime))
                result = Cursor.fetchone()
                Cursor.close()
                Connection.close()
                if result:
                    self.__TimeSlot_ID = result[0]
                    return self.__TimeSlot_ID
                else:
                    return None
            except Exception as e:
                print("Error getting time slot ID:", e)
                return None
      
    def __Insert(self):  
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
            Connection = connect()
            Cursor = cursor(Connection)
            query = "SELECT * FROM TimeSlot"
            Cursor.execute(query)
            result = Cursor.fetchall()
            Cursor.close()
            Connection.close()
            print(result)
            return True
        except Exception as e:
            print(e)
            return False
    
    @staticmethod
    def FindTimeSlot(Host_ID):
        try:
            Connection = connect()
            Cursor = cursor(Connection)
            query = "SELECT * FROM TimeSlot WHERE Host_ID = %s"
            Cursor.execute(query, (Host_ID,))
            result = Cursor.fetchone()
            Cursor.close()
            Connection.close()
            return result
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def FindFreeTimeSlotsForUser(Host_ID):
        try:
            Connection = connect()
            Cursor = cursor(Connection)
            query = "SELECT TimeSlot_ID FROM TimeSlot WHERE Host_ID = %s AND State = 'Free'"
            Cursor.execute(query, (Host_ID,))
            result = [item[0] for item in Cursor.fetchall()]
            Cursor.close()
            Connection.close()
            return result
        except Exception as e:
            print(e)
            return []
    

    @staticmethod
    def BookTimeSlot(TimeSlot_ID, Client_ID):
        """
        Book an existing free time slot for a client using transaction with row locking.
        
        Uses SELECT FOR UPDATE to lock the row and prevent race conditions
        when multiple users try to book the same slot simultaneously.
        
        Returns:
            True  - if booking succeeded
            False -if  timeslot doesn't exist, already booked, or error
        """
        Connection = None
        Cursor = None
        try:
            Connection = connect()
            Cursor = cursor(Connection)
            
            # Disable autocommit to start a transaction
            Connection.autocommit = False
            
            # Step 1: Lock the row with SELECT FOR UPDATE
            # This prevents other transactions from modifying this row until we commit
            Cursor.execute("""
                SELECT TimeSlot_ID, State FROM TimeSlot 
                WHERE TimeSlot_ID = %s 
                FOR UPDATE
            """, (TimeSlot_ID,))
            
            row = Cursor.fetchone()
            
            # Check if timeslot exists
            if row is None:
                Connection.rollback()
                print("TimeSlot not found")
                return False
            
            # Check if timeslot is still free
            if row[1] != 'Free':
                Connection.rollback()
                print("TimeSlot is already booked")
                return False
            
            # Step 2: Update the TimeSlot
            Cursor.execute("""
                UPDATE TimeSlot 
                SET Client_ID = %s, 
                    State = 'Booked', 
                    BookedAt = NOW() 
                WHERE TimeSlot_ID = %s
            """, (Client_ID, TimeSlot_ID))
            
            # Step 3: Create the Meeting record
            Cursor.execute("""
                INSERT INTO Meeting (TimeSlot_ID, State) 
                VALUES (%s, 'Scheduled')
            """, (TimeSlot_ID,))
            
            # Commit the transaction - releases the lock
            Connection.commit()
            return True
            
        except Exception as e:
            # Rollback on any error
            if Connection:
                Connection.rollback()
            print("Error booking timeslot:", e)
            return False
            
        finally:
            # Always close cursor and connection
            if Cursor:
                Cursor.close()
            if Connection:
                Connection.close()

