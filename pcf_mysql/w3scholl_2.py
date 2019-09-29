import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'pcf_user',
    passwd = '4568',
    database = 'pcf_database_1'
)

mycursor = mydb.cursor()

sql = "INSERT INTO cows (cow_id, date_time) VALUES (%s, %s)"
val = ("1234567890", "13.08.2019 - 19:30")
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount,"record inserted.")