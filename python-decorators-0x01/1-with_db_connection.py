import sqlite3
import functools

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        #open the db connection
        conn = sqlite3.connect('users.db')
        
        #pass to function
        try:
            return func(conn, *args, **kwargs)
        finally:
            #close
            conn.close()
    
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

user = get_user_by_id(user_id=1)
print(user)
