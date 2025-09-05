import mysql.connector

# connect to the db
def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='yosemite',
            database='ALX_prodev'
        )
        return connection # returns the connection object
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# stream the rows
def stream_users():
    connection = connect_db()
    if connection:
        cursor = connection.cursor(dictionary=True)  
        cursor.execute("SELECT * FROM user_data;")

        # emit one row at a time
        for row in cursor:
            yield row  
        
        cursor.close()
        connection.close()
