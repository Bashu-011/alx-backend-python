import sqlite3
import functools
import logging

# loging setup
logging.basicConfig(level=logging.INFO)

def log_queries(func):
    @functools.wraps(func) 
    def wrapper(*args, **kwargs):
        query = args[0]
        logging.info(f"Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper

#db connection
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

users = fetch_all_users(query="SELECT * FROM users")
print(users)
