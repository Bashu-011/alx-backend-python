import mysql.connector

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

#function to stream users
def stream_users_in_batches(batch_size):
    connection = connect_db()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")

        #get the rows in batches
        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break #for the last row
            yield rows

        cursor.close()
        connection.close()
    
# function to filter the batches
def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user) 