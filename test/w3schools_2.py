import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="7474"
)

print(mydb)