"""sql_databases.py - это модуль для хранения данных, которые не были отправлены на сервер в базе данных.

 Edition by Suieubayev Maxat.
 Contact number +7 775 818 48 43. Email maxat.suieubayev@gmail.com"""

#!/usr/bin/sudo python3

import feeder_module as fdr
import config as cfg
import sqlite3
import os
from loguru import logger
import requests
import json

def __tableCheck():                               # Функция для создания таблицы если ее не существует
    try:
        db = sqlite3.connect('server.db')                # Создание объекта (соединение с базой данных)
        sql = db.cursor()  
        sql.execute("""CREATE TABLE IF NOT EXISTS json_data (
            id INTEGER,
            Eventdatetime TEXT,
            EquipmentType TEXT,
            SerialNumber TEXT,
            FeedingTime REAL,
            RFIDNumber TEXT,
            WeightLambda REAL,
            FeedWeight REAL) """)

        db.commit()                                 # Обязательно делать коммит при внесении изменений в таблице
        sql.close()
    except ValueError as v:
        logger.error(f'sql.py __tableCheck function: {v}')
    finally:
        if db:
            db.close()


def __countId():                                   # Введение счета id 
    try:
        db = sqlite3.connect('server.db')          # Создание объекта (соединение с базой данных)
        sql = db.cursor()  
        path = 'config.ini'
        if not os.path.exists(path):
            cfg.create_config()
        dbid = int(cfg.get_setting("DbId", "id"))  # Забираем id
        dbid += 1                                  # Увеличиваем на 1
        cfg.update_setting("DbId", "id", str(dbid))     # Записываем в конфиг новый id
        sql.close()
        return dbid
    except ValueError as e:
        logger.error(f'sql.py, count Id function: {e}')
    finally:
        if db:
            db.close()


def __tableValuesConvert(payload):            # Функция конвертации из json в отдельные переменные
    try:
        eventdatetime = payload['Eventdatetime']
        equipmentType = payload["EquipmentType"]
        serialNumber = payload["SerialNumber"]
        feedingTime = payload["FeedingTime"]
        rfidNumber = payload["RFIDNumber"]
        weightLambda = payload["WeightLambda"]
        feedWeight = payload["FeedWeight"]
        return eventdatetime, equipmentType, serialNumber, feedingTime, rfidNumber, weightLambda, feedWeight
    except ValueError as e:
        logger.error(f'sql.py, table values convert function: {e}')


def __tableInsertData(payload):           # Функция для добавления значении в базу данных
                                          # payload передается из main (json строка)
    try:
        db = sqlite3.connect('server.db')                # Создание объекта (соединение с базой данных)
        sql = db.cursor()  
        __tableCheck()
        eventdatetime, equipmentType, serialNumber, feedingTime, rfidNumber, weightLambda, feedWeight = __tableValuesConvert(payload)
        sql.execute("INSERT INTO json_data VALUES(?,?,?,?,?,?,?,?));", 
        __countId(), eventdatetime, equipmentType, serialNumber, feedingTime, rfidNumber, weightLambda, feedWeight)
        db.commit()
        sql.close()
    except ValueError as e:
        logger.error(f'sql.py, table insert data function: {e}')
    finally:
        if db:
            db.close()


def noInternet(payload):                # Функция которая пойдёт в main();
    try:
        if payload:
            __tableInsertData(payload)
        else:
            logger.error(f'sql.py, no internet function payload: {payload}')
    except ValueError as e:
        logger.error(f'sql.py, no internet function: {e}')



def __takeFirstData():                  # Забираем из базы данных первую строку
    try:
        db = sqlite3.connect('server.db')                # Создание объекта (соединение с базой данных)
        sql = db.cursor()
        sql.execute("SELECT * FROM json_data")
        row = sql.fetchone()
        sql.close()
        return row
    except ValueError as e:
        logger.error(f'sql.py, __takefirstdata function: {e}')
    finally:
        if db:
            db.close()


def __convertDataFromTable():           # Готовим переменные для отправки на сервер
    try:
        savedData = __takeFirstData()
        id = savedData[0]
        event_time = savedData[1]
        feed_time = savedData[4]
        animal_id = savedData[5]
        end_weight = savedData[6]
        feed_weight = savedData[7]
        payload = fdr.post_request(event_time, feed_time, animal_id, end_weight, feed_weight)
        return id, payload                  # Возвращаем json строку
    except ValueError as e:
        logger.error(f'sql.py, __convertDataFromTable function: {e}')


def __deleteSavedData(id):              # Удаление отправленной инфы
    try:
        db = sqlite3.connect('server.db')                # Создание объекта (соединение с базой данных)
        sql = db.cursor()
        sql.execute(f"""DELETE from json_data WHERE id = {id}""")
        db.commit()
        sql.close()
    except ValueError as e:
        logger.error(f'sql.py, deleteSavedData function: {e}')
    finally:
        if db:
            db.close()
            

def __sendSavedData():                # Функция отправки инфы на сервер
    try:
        url = "https://smart-farm.kz:8502/api/v2/RawFeedings"
        headers = {'Content-type': 'application/json'}
        id, post_data = __convertDataFromTable()
        post = requests.post(url, data = json.dumps(post_data), headers = headers, timeout=5)
        post.raise_for_status()
    except ValueError as e:
        logger.error(f'sql.py, __sendSavedData function: {e}')
    else:
        __deleteSavedData(id)


def internetOn():
    try:
        db = sqlite3.connect('server.db')                # Создание объекта (соединение с базой данных)
        sql = db.cursor()
        count = sql.execute("SELECT COUNT(SerialNumber) FROM json_data").fetchall()
        tableLen = count[0][0]
        if tableLen>0:
            __sendSavedData()
        sql.close()

    except ValueError as e:
        logger.error(f'Error, check data table function: {e}')
    finally:
        if db:
            db.close()


