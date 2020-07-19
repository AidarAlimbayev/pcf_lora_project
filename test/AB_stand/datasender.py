#!/usr/bin/sudo python3
import sqlite3
from datetime import datetime
import time
import socket
import json
import requests

def Send_data_to_server(): # Отправка данных на сервер КАТУ по JSON
    conn = 0
    cursor = 0

    try:
        print("Try to connect to database")
        conn = sqlite3.connect("mydb.db")
        cursor = conn.cursor()
        print("Sucessfully connected to database")
    except Exception:
        print("Could not connect to database")

    while(1):
        time.sleep(1)
        sql = """Select * FROM cow_weight WHERE sended = 0 ORDER BY id"""
        rows = cursor.execute(sql)

        for row in rows:
            print(row)
            row_id = row[0]
            animal_id = row[1]
            weight_finall = row[2]
            type_scales = row[4]

            print("lib:RFID_reader: Start sending DATA TO SERVER:")
            # logging.info("lib:RFID_reader: Start sending DATA TO SERVER:")
            url = 'http://194.4.56.86:8501/api/weights'
            headers = {'Content-type': 'application/json'}
            data = {"AnimalNumber" : animal_id,
                    "Date" : str(datetime.now()),
                    "Weight" : weight_finall,
                    "ScalesModel" : type_scales}
            
            response = requests.Response()
            response.status_code = 404
            try:
                while response.status_code != 200:
                    print('Sending request')
                    response = requests.post(url, data=json.dumps(data), headers=headers)
                    # logging.info("lib:RFID_reader: Answer from server: ")
                    # logging.info(answer) # можно ли как-то на этой строке остановиться вдебаге?
                    print("lib:RFID_reader: Answer from server: %s" % response)
                    time.sleep(1)

                print("Sended successfully")
                sql = """UPDATE cow_weight SET sended = 1 WHERE id = %d""" % row_id
                cursor.execute(sql)
                conn.commit()
            except Exception as e:
                print(e)
                print("Could not send data to server")
                # logging.info("lib:RFID_reader: Err send data to server")
                # logging.info(e)



Send_data_to_server()