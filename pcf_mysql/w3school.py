import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="pcf_user",
  passwd="4568"
)

mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")

for x in mycursor:
  print(x) 