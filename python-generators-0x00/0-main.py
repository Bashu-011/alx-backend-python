#!/usr/bin/python3
import seed

connection = seed.connect_db()
if connection:
    seed.create_database(connection)
    connection.close()
    print("Connection successful!")

     # Connect to ALX_prodev
    connection = seed.connect_to_prodev()
    if connection:
        seed.create_table(connection)
        seed.insert_data(connection, 'user_data.csv')

        for row in seed.stream_rows(connection):
            print(row)

            connection.close()
