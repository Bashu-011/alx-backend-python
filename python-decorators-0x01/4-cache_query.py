import time
import sqlite3
import functools

# cache storing query as key, value is the result
query_cache = {}

#db connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    
    return wrapper

#decorator to store query cashe
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
       #checking if query has been cached
        if query in query_cache:
            print("Using cached result")
            return query_cache[query]  
        else:
            #else run query
            result = func(conn, query, *args, **kwargs)
            query_cache[query] = result  #store response in cache
            print("Caching result for query")
            return result
    return wrapper

#test
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
