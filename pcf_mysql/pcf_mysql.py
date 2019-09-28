import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "pcf_user_mysql",
    passwd = "pcf_user_mysql"
)

print(mydb)