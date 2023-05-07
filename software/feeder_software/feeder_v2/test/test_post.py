#!/usr/bin/python3
import datetime
import json

from requests.exceptions import HTTPError
import timeit
import requests
from loguru import logger 
import datetime


type_scales = "Scales_10_test"

logger.add('feeder.log', format="{time} {level} {message}", 
level="DEBUG", rotation="1 day", compression="zip")  

def post_request():
    try:
        feeder_type = "Feeder"
        serial_number = 'feeder0423v21-1-test'
        payload = {
            "Eventdatetime": str(str(datetime.datetime.now())),
            "EquipmentType": feeder_type,
            "SerialNumber": serial_number,
            "FeedingTime": str((timeit.default_timer() + 10) - timeit.default_timer()),
            "RFIDNumber": "animal_id_feeder_test_05.2023",
            "WeightLambda": 150,
            "FeedWeight": 100
        }
        return payload
    except ValueError as v:
        logger.error(f'Post_request function error: {v}')

def send_post(postData):
    url = "https://smart-farm.kz:8502/api/v2/RawFeedings"
    headers = {'Content-type': 'application/json'}
    try:
        post = requests.post(url, data = json.dumps(postData), headers = headers, timeout=30)
        logger.info(f'Status Code {post.status_code}')
    except HTTPError as http_err:
        logger.error(f'HTTP error occurred: {http_err}')
    except Exception as err:
        logger.error(f'Other error occurred: {err}')

@logger.catch
def main_test():
    try:
        send_post(post_request())
    except HTTPError as http_err:
        logger.error(f'HTTP error occurred: {http_err}')


main_test()