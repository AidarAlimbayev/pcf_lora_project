import numpy
import requests
import json
#import feeder_test as fdr
from requests.exceptions import HTTPError
from loguru import logger
from datetime import datetime   

feeder_type = "feeder_model_1"
type = "Feeder"
serial_number = "65545180001"
animal_id = "b'435400040001'"       #???????????????????
null_id = "b'435400040001'"         #???????????????????
weight_finall = 0                   #???????????????????
url = "https://smart-farm.kz:8502/api/v2/RawFeedings"
headers = {'Content-type': 'application/json'}

feed_time_rounded = 61.6
final_weight_rounded, end_weight_rounded = 151.11, 85.1

def post_request(feeder_type, serial_number, feed_time, animal_id, end_weight, feed_weight):
        payload = {
            "Eventdatetime": str(datetime.now()),
            "EquipmentType": feeder_type,
            "SerialNumber": serial_number,
            "FeedingTime": feed_time,
            "RFIDNumber": animal_id,
            "WeightLambda": end_weight,
            "FeedWeight": feed_weight
        }
        return payload

post_data = post_request(feeder_type, serial_number, feed_time_rounded, animal_id, final_weight_rounded, end_weight_rounded)
try:
    post = requests.post(url, data = json.dumps(post_data), headers = headers, timeout=0.5)
    post.raise_for_status()
except HTTPError as http_err:
    logger.error(f'HTTP error occurred: {http_err}')
except Exception as err:
    logger.error(f'Other error occurred: {err}')

