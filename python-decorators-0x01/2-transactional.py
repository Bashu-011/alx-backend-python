import sqlite3
import functools

# decorator for db_connections
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
                
        try:
            return func(conn, *args, **kwargs)  
        finally:
            conn.close()
    
    return wrapper

# decorator to manage db transactions
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            print(f"Error occurred: {e}, rolling back transaction")
            raise  
    return wrapper

#test function
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

try:
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
    print("User email updated successfully")
except Exception as e:
    print("Failed to update email:", e)
