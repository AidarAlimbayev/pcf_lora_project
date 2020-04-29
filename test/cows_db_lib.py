#cows_db_lib.py
# Библиотека функций обращений к базам 

import sqlite3
from sqlite3 import Error
from cows_tables_classes import Cow
from cows_tables_classes import Raw_data
from cows_tables_classes import Processed_data
import tables_for_create_base #может быть пригодится

conn = sqlite3.connect('cows_database.db')  #conn = sqlite3.connect(':memory:') # как альтернатива
c = conn.cursor()

cow_1 = Cow(1, 123, 300.1, '14 days', 'after 14 days', '300 min') # Пример в таблицу cow
raw_data_1 = Raw_data(3, 11, 300.9, '2:45 AM') # Пример в таблицу raw_data
processed_data_1 = Processed_data(1, 22, 300, '30.05.2020') # Пример в таблицу processed_data

#----------------------------------------------------------------------------
# Функции для основной таблицы
def insert_cow(id, rf_id, weight, spray_period, next_spray_time, last_drink_duration):
    with conn:
        c.execute("INSERT INTO cow VALUES (INSERT INTO raw_data VALUES (:id, :cow_id, :weight, :timestamp)", {'id':raw_data_1.id, 'cow_id':raw_data_1.cow_id, 'weight':raw_data_1.weight, 'timestamp':raw_data_1.timestamp})
        
def get_cow_by_rf_id(rf_id):
    with conn:
        c.execute("SELECT * FROM cow VALUES ()")

def get_cow_by_id(id):
    pass

#----------------------------------------------------------------------------
# Функции для таблицы сырых данных
def insert_raw_data(id, cow_id,  weight, timestamp):
    pass

def get_raw_data_by_cow_id(cow_id):
    pass

def get_raw_data_by_id(id):
    pass

#----------------------------------------------------------------------------
# Функции для таблицы обработанных данных
def insert_processed_data(id, cow_id,  weight, timestamp):
    pass

def get_processed_data_by_cow_id(cow_id):
    pass

def get_processed_data_by_id(id):
    pass

def update_processed_data(id, cow_id,  weight, timestamp):
    pass


#----------------------------------------------------------------------------
# Функции для удалениея данных из таблиц
def remove_cow():
    pass
def remove_raw_data():
    pass
def remove_processed_data():
    pass
#----------------------------------------------------------------------------


cow_1 = Cow(1, 123, 300.1, '14 days', 'after 14 days', '300 min') # Пример в таблицу cow
raw_data_1 = Raw_data(3, 11, 300.9, '2:45 AM') # Пример в таблицу raw_data
processed_data_1 = Processed_data(1, 22, 300, '30.05.2020') # Пример в таблицу processed_data
# print(cow_1.id)
# print(raw_data_1.weight)
# print(processed_data_1.timestamp)

# c.execute("INSERT INTO cow VALUES (?, ?, ?, ?, ?, ?)", (cow_1.id, cow_1.rf_id, cow_1.weight, cow_1.spray_period, cow_1.next_spray_time, cow_1.last_drink_duration))

# conn.commit()

# c.execute("INSERT INTO raw_data VALUES (:id, :cow_id, :weight, :timestamp)", {'id':raw_data_1.id, 'cow_id':raw_data_1.cow_id, 'weight':raw_data_1.weight, 'timestamp':raw_data_1.timestamp})

# conn.commit()

c.execute("SELECT * FROM raw_data WHERE cow_id = ?", (11,))

print(c.fetchall())

conn.close()