import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "Aidar",
    password = "123"
)













































# #sqlite_tutorial_1.py

# import sqlite3
# from sqlite3 import Error


# def create_connection(db_file):
#     """ create a database connection to the SQLite database
#         specified by db_file
#     :param db_file: database file
#     :return: Connection object or None
#     """
#     conn = None
#     try:
#         conn = sqlite3.connect(db_file)
#         return conn
#     except Error as e: 
#         print(e)
        
#     return conn

# def create_table(conn, create_table_sql):
#     """create a table from the create_table_sql statement
#     :param conn: Connection object
#     :param create_table_sql: a CREATE TABLE statement
#     :return:
#     """
#     try:
#         c = conn.cursor()
#         c.execute(create_table_sql)
#     except Error as e:
#         print(e)
    
#     return conn

# def create_table(conn, create_table_sql):
#     """create a table from the create_table_sql statement
#     :param conn: Connection object
#     :param create_table_sql: a CREATE TABLE statement
#     :retrun:
#     """
#     try:
#         c = conn.cursor()
#         c.execute(create_table_sql)
#     except Error as e:
#         print(e)

# def main():
#     database = "db_file.db"

#     sql_create_projects_table = """CREATE TABLE IF NOT EXISTS projects (
#                                 id integer PRIMARY KEY,
#                                 name text NOT NULL,
#                                 begin_date text,
#                                 end_date text
#                                 ); """

#     sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
#                                 id integer PRIMARY KEY,
#                                 name text NOT NULL,
#                                 priority integer,
#                                 status_id integer NOT NULL,
#                                 project_id integer NOT NULL,
#                                 begin_date text NOT NULL,
#                                 end_date text NOT NULL,
#                                 FOREIGN KEY (project_id) REFERENCES projects (id)
#                                 ); """

#     conn = create_connection(database)

#     if conn is not None:
#         create_table(conn, sql_create_projects_table)
#         create_table(conn, sql_create_tasks_table)
#     else:
#         print("Error! cannor create the database connection.")

# if __name__=='__main__':
#     main()

                