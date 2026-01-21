import mysql.connector
from dotenv import load_dotenv
load_dotenv(override=True)
import os
host=os.getenv("host")
user=os.getenv("username")
password=os.getenv("password")
database=os.getenv("database")
def connect():
    try :
        connection=mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return connection
    except Exception as e:
        print(e)
        return None
def cursor(connection):
    try:
        if connection is None:
            print("Connection is None, cannot create cursor")
            return None
        cursor = connection.cursor()
        return cursor
    except Exception as e:
        print(e)
        return None

def close(connection, cursor):
    try:
        if connection is None or not connection.is_connected():
            return False
        if cursor is not None:
            cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(e)
        return False