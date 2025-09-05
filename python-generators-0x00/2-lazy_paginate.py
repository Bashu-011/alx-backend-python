import seed
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

def paginate_users(page_size, offset):
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows

def lazy_paginate(page_size):
    offset = 0  # get the first page
    while True:
        # next pages
        page = paginate_users(page_size, offset)
        if not page:
            break  # end of rows
        yield page  
        offset += page_size  
