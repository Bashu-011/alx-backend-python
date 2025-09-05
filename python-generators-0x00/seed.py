import mysql.connector
import csv

def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='yosemite'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# create db if it does not exist
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    print("Database ALX_prodev created or already exists.")
    cursor.close()

#connect to the db
def connect_to_prodev():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='yosemite',
        database='ALX_prodev'
    )
    return connection

#create table
def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_data (
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age INT NOT NULL
    );
    """)
    print("Table user_data created successfully.")
    cursor.close()

#inserting the data
def insert_data(connection, filename):
    cursor = connection.cursor()
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # skip the titles
        for row in csv_reader:
            cursor.execute("""
            INSERT INTO user_data (name, email, age)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
            name=VALUES(name), email=VALUES(email), age=VALUES(age);
            """, (row[0], row[1], row[2]))
        connection.commit()
    print("Data inserted successfully.")
    cursor.close()

#stream rows into the db
def stream_rows(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data;")
    
    #fetch rows
    rows = cursor.fetchall()
    
    if not rows:
        print("No rows found in the user_data table.")
        cursor.close()
        return
    
    
    for row in rows:
        print(f"Streaming row: {row}")  # for debugging
        yield row 
    
    cursor.close()

# code to run 
if __name__ == "__main__":
    connection = connect_db()
    if connection:
        create_database(connection)
        connection.close()
        print("Connection successful!")

        # connect to the db
        connection = connect_to_prodev()
        if connection:
            create_table(connection)
            insert_data(connection, 'user_data.csv')

            # for debugging, stream rows and print
            for row in stream_rows(connection):
                print(row)

            connection.close()
