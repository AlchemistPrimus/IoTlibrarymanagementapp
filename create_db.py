import mysql.connector
import os

password=os.environ.get("PASSWORD")
mydb=mysql.connector.connect(host="127.0.0.1",user="root",passwd="password",auth_plugin='mysql_native_password')

my_cursor=mydb.cursor()
my_cursor.execute("CREATE DATABASE lib_data")
my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)