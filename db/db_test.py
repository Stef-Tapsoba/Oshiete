import os
import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1", #host = "db" in the final version
    port="33065",
    user="root",
    passwd = "example",
    database = "info600"
)

my_cursor = mydb.cursor()

my_cursor.execute("SELECT name, email FROM users")
records = my_cursor.fetchall()

for record in records:
    print(record)