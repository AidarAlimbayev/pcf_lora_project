#sqlite_tutorial_deleting_date.py
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """create a database connection to the SQLite database
    specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None 
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def delete_task(conn, id):
    """
    Delete a task by task id
    :param conn: connection to the SQLite database
    :param id: id of the task
    :return: 
    """
    sql = 'DELETE FROM tasks WHERE id = ?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

def delete_all_tasks(conn):
    """
    Delete all rows in the tasks table
    :param conn: connection to the SQLite database
    :return:
    """
    sql = 'DELETE FROM tasks'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def main():
    database = "db_file.db"

    conn = create_connection(database)
    with conn:
        delete_task(conn, 2);

if __name__ == '__main__':
    main()