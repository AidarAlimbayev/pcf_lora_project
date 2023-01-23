import sqlite3
import test as t


db = sqlite3.connect('server.db')
sql = db.cursor()
def once_check():
    sql.execute("""CREATE TABLE IF NOT EXISTS json_data (
        id INTEGER,
        Eventdatetime TEXT,
        EquipmentType TEXT,
        SerialNumber TEXT,
        FeedingTime REAL,
        RFIDNumber TEXT,
        WeightLambda REAL,
        FeedWeight REAL) """)

    db.commit()

once_check()

user_serial = input("SerialNumber: ")
user_eqtype = input("EqType: ")

sql.execute(f"SELECT Eventdatetime from json_data WHERE SerialNumber = '{user_serial}'")

if sql.fetchone() is None:
    sql.execute(f"INSERT INTO json_data VALUES (?, ?, ?, ?, ?, ?, ?)", ('12/12/2022', user_eqtype, user_serial,  50.6, '040000444', 1.121, 44.85))
    db.commit()
    print('Reg-ed') 
else:
    print("Here we have something!")
   # for value in sql.execute("SELECT * FROM json_data"):
   #     print(value)

coun = sql.execute("SELECT COUNT(SerialNumber) FROM json_data").fetchall()
print(coun[0][0])

con = sql.execute("SELECT * FROM json_data")
row = sql.fetchone()
sql.execute("DELETE FROM json_data WHERE SerialNumber = '11111'")
