import sqlite3

class ExecuteQuery:
    # initialize with query and arameters as the contructors
    def __init__(self, query, params):
        self.query = query 
        self.params = params  

    #open the db connection
    def __enter__(self):
        self.conn = sqlite3.connect('users.db')  
        self.cursor = self.conn.cursor()
        return self.cursor  

#log exception
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"An exception occurred: {exc_val}")
        
        self.conn.close()

#test
query = "SELECT * FROM users WHERE age > ?"
params = (25,)  

with ExecuteQuery(query, params) as cursor:
    cursor.execute(query, params) 
    results = cursor.fetchall()  
    print(results) 