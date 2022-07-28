"""Feeder version 1. Edition by Suieubayev Maxat.
Contact number +7 775 818 48 43. Email maxat.suieubayev@gmail.com"""
#!/usr/bin/sudo python
from turtle import fd
import feeder_test.feeder_test as fdr
import lib_pcf_spray as pcf
import timeit
import requests
import json
import datetime
from requests.exceptions import HTTPError


pcf.time.sleep(10)

feeder_type = "feeder_model_1"
type = "FEEDER"
serial_number = "65545180001"

animal_id = "b'435400040001'"
null_id = "b'435400040001'"
weight_finall = 0
url = "https://smart-farm.kz:8502/api/v2/RawFeedings"
headers = {'Content-type': 'application/json'}


try:
    s = pcf.serial.Serial('/dev/ttyACM0',9600) 
    pcf.print_log(f'Connect arduino {s.name}')
    pcf.print_log(f'Configuration of serial: {s}')
except Exception as e:
    pcf.print_log(f'Error to connection to arduino, there is no file: /dev/ttyACM0 {e}')
else:
    pcf.print_log(f'Success: Arduino connected')

def main():
    while True:
        dist = fdr.distance()
        distance = fdr.measuring_start(dist)
        if distance is True:
            start_weight = fdr.instant_weight(s)
            start_time = timeit.default_timer
            animal_id = fdr.rfid_label()
            pcf.print_log(f'First step cow ID :{animal_id}')

            pcf.time.sleep(1)
            
            if animal_id != '435400040001': 
                pcf.print_log(f'After read cow ID :{animal_id}')
                while distance is True:
                    end_time = timeit.default_timer
                    end_weight = fdr.instant_weight(s)
                feed_time = int(start_time) - int(end_time)
                final_weight = int(start_weight) - int(end_weight)
                post_data = fdr.post_request(feeder_type, serial_number, feed_time, animal_id, final_weight, end_weight)
                try:
                    post = requests.post(url, data = json.dumps(post_data), headers = headers, timeout=0.5)
                    post.raise_for_status()
                except HTTPError as http_err:
                    pcf.print_log(f'HTTP error occurred: {http_err}')
                except Exception as err:
                    pcf.print_log(f'Other error occurred: {err}')
