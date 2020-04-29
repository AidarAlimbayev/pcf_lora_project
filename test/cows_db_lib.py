#cows_db_lib.py
# Библиотека функций обращений к базам 

import sqlite3
from sqlite3 import Error
from cows_tables_classes import Cow
from cows_tables_classes import Raw_data
from cows_tables_classes import Processed_data
import tables_for_create_base #может быть пригодится

conn = sqlite3.connect('db_file.db')

c = conn.cursor()

cow_1 = Cow(1, 123, 300.1, '14 days', 'after 14 days', '300 min')

raw_data_1 = Raw_data(1, 11, 300.2, '2:19 AM')

processed_data_1 = Processed_data(1, 22, 300, '30.05.2020')


print(cow_1.id)
print(raw_data_1.weight)
print(processed_data_1.timestamp)

c.execute("INSERT INTO cow VALUES ")

conn.commit()

conn.close()