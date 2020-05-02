#cows_db_lib.py
# Библиотека функций обращений к базам 

import sqlite3
import datetime as dt
from sqlite3 import Error
from cows_tables_classes import Cow_class
from cows_tables_classes import Raw_data_class
from cows_tables_classes import Processed_data_class
import tables_for_create_base #может быть пригодится

conn = sqlite3.connect('cows_database.db')  #conn = sqlite3.connect(':memory:') # как альтернатива
c = conn.cursor()

# cow_1 = Cow_class(123, 300.1, '14 days', 'after 14 days', '300 min') # Пример в таблицу cow
# raw_data_1 = Raw_data(3, 11, 300.9, '2:45 AM') # Пример в таблицу raw_data
# processed_data_1 = Processed_data(1, 22, 300, '30.05.2020') # Пример в таблицу processed_data

#----------------------------------------------------------------------------
# Функции для основной таблицы
def insert_cow(rf_id, weight, spray_period, next_spray_time, last_drink_duration):
    with conn:
        c.execute("INSERT INTO cow(rf_id, weight, spray_period, next_spray_time, last_drink_duration) VALUES (?, ?, ?, ?, ?);", (rf_id, weight, spray_period, next_spray_time, last_drink_duration))
        return("cow data inserted")

def get_cow_by_id(id):
    with conn:
        c.execute("SELECT * FROM cow WHERE id = ?;", (id,))
        return c.fetchall()
        
def get_cow_by_rf_id(rf_id):
    with conn:
        c.execute("SELECT * FROM cow WHERE rf_id = ?;", (rf_id,))
        return c.fetchall()

#----------------------------------------------------------------------------
# Функции для таблицы сырых данных
def insert_raw_data(cow_id, weight):
    with conn:
        c.execute("INSERT INTO raw_data(cow_id, weight, timestamp) VALUES (?, ?, datetime('now'));", (cow_id, weight,))
        return("raw data inserted")

def get_raw_data_by_id(id):
  with conn:
        c.execute("SELECT * FROM raw_data WHERE id = ?;", (id,))
        return c.fetchall()

def get_raw_data_by_cow_id(cow_id):
  with conn:
        c.execute("SELECT * FROM raw_data WHERE cow_id = ?;", (cow_id,))
        return c.fetchall()

#----------------------------------------------------------------------------
# Функции для таблицы обработанных данных
def insert_processed_data(id, cow_id,  weight, timestamp):
    pass

def get_processed_data_by_cow_id(cow_id):
    pass

def get_processed_data_by_id(id):
    pass

#def update_processed_data(id, cow_id,  weight, timestamp): # обновление данных в таблице обработанных данных
#    with conn:
#        c.execute("""UPDATE processed_data SET weight = :weight AND timestamp =: timestamp WHERE cow_id =: cow_id""", 
#        {'id'.id, 'cow_id':processed_data_1.cow_id, 'weight':processed_data_1.weight, 'timestamp':processed_data_1.timestamp})


#----------------------------------------------------------------------------
# Функции для удалениея данных из таблиц
def remove_cow():
    pass
def remove_raw_data():
    pass
def remove_processed_data():
    pass
#----------------------------------------------------------------------------

# тест библиотеки 

# print(cow_1)

# cow_1 = Cow_class(123, 300.1, '14 days', 'after 14 days', '300 min')

#print(insert_cow(124, 321.1, '7 days', 'after 6 days', '500 min'))

print(insert_raw_data(7, 377.12))

#c.execute("SELECT * FROM cow")

print(get_cow_by_id(7))

print(get_cow_by_rf_id(122))

#print(c.fetchall())

conn.commit()
conn.close()

# cow_1 = Cow(3, 133, 330.1, '14 days', 'after 14 days', '300 min') # Пример в таблицу cow
# raw_data_1 = Raw_data(3, 11, 300.9, '2:45 AM') # Пример в таблицу raw_data
# processed_data_1 = Processed_data(1, 22, 400, '30.05.2020') # Пример в таблицу processed_data
# print(cow_1.id)
# print(raw_data_1.weight)
# print(processed_data_1.timestamp)

# c.execute("INSERT INTO cow VALUES (?, ?, ?, ?, ?, ?)", (cow_1.id, cow_1.rf_id, cow_1.weight, cow_1.spray_period, cow_1.next_spray_time, cow_1.last_drink_duration))

# conn.commit()

# c.execute("INSERT INTO raw_data VALUES (:id, :cow_id, :weight, :timestamp)", {'id':raw_data_1.id, 'cow_id':raw_data_1.cow_id, 'weight':raw_data_1.weight, 'timestamp':raw_data_1.timestamp})

# conn.commit()

# c.execute("SELECT * FROM raw_data WHERE cow_id = ?", (11,))

# print(c.fetchall())

