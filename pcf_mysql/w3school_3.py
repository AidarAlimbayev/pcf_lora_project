import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'pcf_user',
    passwd = '4568',
    database = 'pcf_database_1'
)

mycursor = mydb.cursor()

sql = "INSERT INTO cows(cow_id, cow_weight) VALUES (%s, %s)"
val = [
    ('1234567891', '321'),
    ('1234567892', '322'),
    ('1234567893', '323'),
    ('1234567894', '324'),
    ('1234567895', '325'),
    ('1234567896', '326'),
    ('1234567897', '327'),
    ('1234567898', '328'),
    ('1234567899', '329')
]

mycursor.executemany(sql, val)

mydb.commit()

print(mycursor.rowcount, "was inserted.")