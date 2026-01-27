from src.Core.DB.DataBaseConnection import *

class Meeting:

    def __init__(self,TimeSlot_ID):
        self.TimeSlot_ID = TimeSlot_ID
        self.State = 'Scheduled'
        self.ID = None
        self.__insert()
    
    def __insert(self):
        try:
            Connection = connect()
            Cursor = cursor(Connection)
            Cursor.execute("INSERT INTO Meeting (TimeSlot_ID, State) VALUES (%s, %s)", (self.TimeSlot_ID, self.State))
            Connection.commit()
            self.ID = Cursor.lastrowid
            Cursor.close()
            Connection.close()
            return True
        except Exception as e:
            print("Error inserting meeting:", e)
            return False
    
    def GetMeetingID(self):
        if self.ID is not None:
            return self.ID
        else:
            try :
                Connection = connect()
                Cursor = cursor(Connection)
                Cursor.execute("SELECT ID FROM Meeting WHERE TimeSlot_ID = %s", (self.TimeSlot_ID,))
                result = Cursor.fetchone()
                Cursor.close()
                Connection.close()
                if result:
                    self.ID = result[0]
                    return self.ID
                else:
                    return None
            except Exception as e:
                print("Error getting meeting ID:", e)
                return None
    
    @staticmethod
    def UpdateMeeting(TimeSlot_ID,State):
        try:
            Connection = connect()
            Cursor = cursor(Connection)
            Cursor.execute("UPDATE Meeting SET State = %s WHERE TimeSlot_ID = %s", (State, TimeSlot_ID))
            Connection.commit()
            Cursor.close()
            Connection.close()
            return True
        except Exception as e:
            print("Error updating meeting:", e)
            return False

    @staticmethod
    def CancelMeeting(TimeSlot_ID):
        try:
            Connection = connect()
            Cursor = cursor(Connection)
            Cursor.execute("DELETE FROM Meeting WHERE TimeSlot_ID = %s", (TimeSlot_ID,))
            Connection.commit()
            Cursor.close()
            Connection.close()
            return True
        except Exception as e:
            print("Error canceling meeting:", e)
            return False