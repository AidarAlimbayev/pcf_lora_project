#sqlite_tutorial_insert_data.py

import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """create a database connection to the SQLite databse
    specified by db_file
    :param db_file: database file
    :return: connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    
    return conn

def create_project(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO projects(name, begin_date, end_date)
            VALUES(?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, project)
    return cur.lastrowid


def create_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO
            tasks(name, priority, status_id, project_id,begin_date,end_date)
            VALUES(?, ?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    return cur.lastrowid

def main():
    database = "db_file.db"

    conn = create_connection(database)
    with conn:
        project = ('Cool App with SQLite & Python', '2020-04-28', '2020-04-29');
        project_id = create_project(conn, project)

        task_1 = ('Analyze the requirement of the app', 1, 1, project_id, '2020/04/28', '2020/04/29')
        task_2 = ('Confirm with user about', 1, 1, project_id, '2020/05/01', '2020/04/02')

        create_task(conn, task_1)
        create_task(conn, task_2)


if __name__ == '__main__':
    main()
