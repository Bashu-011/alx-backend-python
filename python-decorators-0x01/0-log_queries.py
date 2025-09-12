import sqlite3
import functools
import logging
from datetime import datetime  # date time correction

# setup loging
logging.basicConfig(level=logging.INFO)

# the decorator to log
def log_queries(func):
    @functools.wraps(func) 
    def wrapper(*args, **kwargs):
        query = args[0]  
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
        logging.info(f"[{timestamp}] Executing SQL Query: {query}")  
        return func(*args, **kwargs)
    return wrapper

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
