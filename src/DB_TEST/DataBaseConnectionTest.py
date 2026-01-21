from Core.DB.DataBaseConnection import *
connection = connect()
if connection is not None:
    print("Connected to the database successfully")
    cursor = cursor(connection)
    if cursor is not None:
        print("Cursor created successfully")
        closed = close(connection, cursor)
        if closed:
            print("Closed the connection successfully")
        else:
            print("Error closing the connection")
    else:
        print("Failed to create cursor")
else:
    print("Failed to connect to the database")