
import sqlite3
from sqlite3 import Error



def create_connection(cows_database):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(cows_database)
        return conn
    except Error as e: 
        print(e)
        
    return conn

def create_table(conn, create_table_sql):
    """create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit() # Добавленная мною строка, может быть лишняя
    except Error as e:
        print(e)
    
    return conn

    
def main():
    database = "cows_database.db"   
        
    sql_create_cow_table = """CREATE TABLE IF NOT EXISTS cow (
                            id integer PRIMARY KEY,
                            rf_id text NOT NULL,
                            weight real NOT NULL,
                            spray_period text NOT NULL,
                            next_spray_time text NOT NULL,
                            last_drink_duration text NOT NULL
                            ); """

    sql_create_raw_data_table = """CREATE TABLE IF NOT EXISTS raw_data (
                                id integer PRIMARY KEY,
                                cow_id integer NOT NULL, 
                                weight real NOT NULL,
                                timestamp text NOT NULL, 
                                FOREIGN KEY (cow_id) REFERENCES cow (id)
                                ); """

    sql_create_processed_data_table = """CREATE TABLE IF NOT EXISTS processed_data (
                                        id integer PRIMARY KEY,
                                        cow_id integer NOT NULL, 
                                        weight real NOT NULL,
                                        timestamp text NOT NULL,
                                        FOREIGN KEY (cow_id) REFERENCES cow (id)
                                        ); """

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_cow_table)
        create_table(conn, sql_create_raw_data_table)
        create_table(conn, sql_create_processed_data_table)
    else:
        print("Error! cannor create the database connection.")

if __name__=='__main__':
    main()




# BEGIN TRANSACTION;
# CREATE TABLE IF NOT EXISTS "Processed_Data" (
# 	"ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
# 	"COW_ID"	TEXT NOT NULL,
# 	"WEIGHT"	NUMERIC NOT NULL,
# 	"TIMESTAMP"	NUMERIC NOT NULL
# );

# CREATE TABLE IF NOT EXISTS "Raw_Data" (
# 	"ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
# 	"COW_ID"	TEXT NOT NULL,
# 	"WEIGHT"	NUMERIC NOT NULL,
# 	"TIMESTAMP"	NUMERIC NOT NULL
# );

# CREATE TABLE IF NOT EXISTS "Cow" (
# 	"ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
# 	"rfidID"	TEXT NOT NULL,
# 	"SprayPeriod"	NUMERIC NOT NULL,
# 	"NextSprayTime"	NUMERIC NOT NULL,
# 	"LastDrinkDuration"	INTEGER NOT NULL
# );
# COMMIT;