from src.Core.DB.DataBaseConnection import *
from datetime import datetime , timedelta

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
    def CancelMeeting(Meeting_ID):
        NOW = datetime.now()
        try:
            Connection = connect()
            Cursor = cursor(Connection)
            # First get the TimeSlot_ID from the Meeting
            Cursor.execute("SELECT TimeSlot_ID FROM Meeting WHERE Meeting_ID = %s", (Meeting_ID,))
            result = Cursor.fetchone()
            if result is None:
                print("Meeting not found")
                Cursor.close()
                Connection.close()
                return False
            TimeSlot_ID = result[0]
            
            # Get StartTime from TimeSlot to check 48-hour rule
            Cursor.execute("SELECT StartTime FROM TimeSlot WHERE TimeSlot_ID = %s", (TimeSlot_ID,))
            StartTime = Cursor.fetchone()[0]
            if(StartTime - NOW < timedelta(hours=48)):
                print("Sorry, You can't cancel the meeting before 48 hours")
                Cursor.close()
                Connection.close()
                return False
            
            # Delete the meeting
            Cursor.execute("DELETE FROM Meeting WHERE Meeting_ID = %s", (Meeting_ID,))
            Connection.commit()
            Cursor.close()
            Connection.close()
            return True
        except Exception as e:
            print("Error canceling meeting:", e)
            return False
    
    @staticmethod
    def ShowAllMeetings():
        try:
            NOW = datetime.now()
            Connection = connect()
            Cursor = cursor(Connection)
            # Join Meeting with TimeSlot to get StartTime and EndTime
            Cursor.execute("""
                SELECT m.Meeting_ID, m.State, m.TimeSlot_ID, ts.StartTime, ts.EndTime
                FROM Meeting m
                JOIN TimeSlot ts ON m.TimeSlot_ID = ts.TimeSlot_ID
            """)
            result = Cursor.fetchall()
            
            updated_results = []
            for row in result:
                Meeting_ID, State, TimeSlot_ID, StartTime, EndTime = row
                
                # Determine the correct state based on current time
                if NOW >= StartTime and NOW <= EndTime:
                    new_state = 'In-Progress'
                elif NOW > EndTime:
                    new_state = 'Ended'
                else:
                    new_state = 'Scheduled'
                
                # Update state in database if it changed
                if new_state != State:
                    Cursor.execute("UPDATE Meeting SET State = %s WHERE Meeting_ID = %s", (new_state, Meeting_ID))
                    Connection.commit()
                
                updated_results.append((Meeting_ID, new_state, TimeSlot_ID, StartTime, EndTime))
            
            Cursor.close()
            Connection.close()
            return updated_results
        except Exception as e:
            print("Error showing meetings:", e)
            return None
    
    @staticmethod
    def ShowAllMeetingsByHostID(Host_ID):
        try:
            NOW = datetime.now()
            Connection = connect()
            Cursor = cursor(Connection)
            # Join Meeting with TimeSlot to get meetings by Host_ID
            Cursor.execute("""
                SELECT m.Meeting_ID, m.State, m.TimeSlot_ID, ts.StartTime, ts.EndTime, ts.Host_ID, ts.Client_ID
                FROM Meeting m
                JOIN TimeSlot ts ON m.TimeSlot_ID = ts.TimeSlot_ID
                WHERE ts.Host_ID = %s
            """, (Host_ID,))
            result = Cursor.fetchall()
            
            updated_results = []
            for row in result:
                Meeting_ID, State, TimeSlot_ID, StartTime, EndTime, Host_ID_val, Client_ID = row
                
                # Determine the correct state based on current time
                if NOW >= StartTime and NOW <= EndTime:
                    new_state = 'In-Progress'
                elif NOW > EndTime:
                    new_state = 'Ended'
                else:
                    new_state = 'Scheduled'
                
                # Update state in database if it changed
                if new_state != State:
                    Cursor.execute("UPDATE Meeting SET State = %s WHERE Meeting_ID = %s", (new_state, Meeting_ID))
                    Connection.commit()
                
                updated_results.append((Meeting_ID, new_state, TimeSlot_ID, StartTime, EndTime, Host_ID_val, Client_ID))
            
            Cursor.close()
            Connection.close()
            return updated_results
        except Exception as e:
            print("Error showing meeting:", e)
            return None