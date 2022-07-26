#!/usr/bin/python
import sqlite3 as sq3

def delete_null_from_zero_table():
    try:
        print("Delete NULL from ZERO table")
        cur = sq3.connect('main_database.db')
        cur.execute("DELETE FROM ZERO WHERE ANIMAL_ID IS NULL OR trim(ANIMAL_ID) = '';") 
        cur.commit()
        cur.close()
    except Exception as e:
        print("Error in Delete NULL from ZERO table function", e)
    else:
        print("Success: Delete NULL from ZERO table")
        return 0

delete_null_from_zero_table()