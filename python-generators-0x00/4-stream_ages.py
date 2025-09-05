import mysql.connector

def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='yosemite',
            database='ALX_prodev'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def stream_user_ages():
    connection = connect_db()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT age FROM user_data;")
        
        for row in cursor:
            yield row['age']
        
        cursor.close()
        connection.close()

def calculate_average_age():
    total_age = 0
    user_count = 0 
    
    for age in stream_user_ages():
        total_age += age
        user_count += 1
    
    if user_count > 0:
        average_age = total_age / user_count
        print(f"Average age of users: {average_age:.2f}")
    else:
        print("No users found.")

