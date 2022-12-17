import test as t
import sqlite3
import os
from loguru import logger
import requests
import json

payload = {
            "Eventdatetime": '',
            "EquipmentType": '',
            "SerialNumber": '',
            "FeedingTime": 0.0,
            "RFIDNumber": '',
            "WeightLambda": 0.0,
            "FeedWeight": 0.0
        }



db = sqlite3.connect('server.db')
sql = db.cursor()

def tableCheck():
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


def countId():
    try:
        path = 'config.ini'
        if not os.path.exists(path):
            t.create_config(path)
        dbid = int(t.config.get("DbId", "id"))
        dbid += 1
        t.update_setting(path, "DbId", "id", str(dbid))
        return dbid
    except ValueError as e:
        logger.error(f'Error, count Id function: {e}')

def tableValuesConvert(payload):
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
        logger.error(f'Error, table values convert function: {e}')



def tableInsertData(payload):
    try:
        tableCheck()
        eventdatetime, equipmentType, serialNumber, feedingTime, rfidNumber, weightLambda, feedWeight = tableValuesConvert(payload)
        sql.execute("INSERT INTO json_data VALUES(?,?,?,?,?,?,?));", 
        countId(), eventdatetime, equipmentType, serialNumber, feedingTime, rfidNumber, weightLambda, feedWeight)
        db.commit()
    except ValueError as e:
        logger.error(f'Error, table values convert function: {e}')


def noInternet(payload):
    try:
        if payload:
            tableInsertData(payload)
        else:
            return 0

    except ValueError as e:
        logger.error(f'Error, no internet function: {e}')


def __takeFirstData():
    try:
        con = sql.execute("SELECT * FROM json_data")
        row = sql.fetchone()
        return row
    except ValueError as e:
        logger.error(f'Error, take first data function: {e}')

def __convertDataFromTable():
    try:
        savedData = __takeFirstData()
        event_time = savedData[1]
        feeder_type = savedData[2]
        serial_number = savedData[3]
        feed_time = savedData[4]
        animal_id = savedData[5]
        end_weight = savedData[6]
        feed_weight = savedData[7]
        payload = t.post_request(event_time, feeder_type, serial_number, feed_time, animal_id, end_weight, feed_weight)
        return payload
    except ValueError as e:
        logger.error(f'Error, __convertDataFromTable function: {e}')

def sendSavedData():
    try:
        url = "https://smart-farm.kz:8502/api/v2/RawFeedings"
        headers = {'Content-type': 'application/json'}
        post_data = __convertDataFromTable()
        post = requests.post(url, data = json.dumps(post_data), headers = headers, timeout=5)
        post.raise_for_status()
    except ValueError as e:
        logger.error(f'Error, send saved data function: {e}')
    else:
        row = __takeFirstData()
        id = row[0]


def checkDataTable():
    try:
        count = sql.execute("SELECT COUNT(SerialNumber) FROM json_data").fetchall()
        tableLen = count[0][0]
        if tableLen>0:
            pass
        else:
            pass
    except ValueError as e:
        logger.error(f'Error, check data table function: {e}')


