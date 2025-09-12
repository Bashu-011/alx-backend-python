import sqlite3

class DatabaseConnection:
    #name o fthe db stored as a variable
    def __init__(self, db_name):
        self.db_name = db_name  

    #establishes a connection and returns the cursor object
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor  

    # to handle errors/exceptions
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"Exception occurred: {exc_val}")
        

        self.conn.close()

#test
with DatabaseConnection('users.db') as cursor:
    cursor.execute("SELECT * FROM users")  
    results = cursor.fetchall()  
    print(results) 
