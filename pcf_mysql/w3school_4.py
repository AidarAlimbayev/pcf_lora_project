import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'pcf_user',
    passwd = '4568',
    database = 'pcf_database_1'
)

mycursor = mydb.cursor()

sql = "INSERT INTO cows(cow_id, cow_weight) VALUES (%s, %s)"
val = ("1234567888", "322")
mycursor.execute(sql, val)

mydb.commit()

print("1 record inserted, ID:", mycursor.lastrowid)
