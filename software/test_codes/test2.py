import threading
import queue
import time
import requests
import json
from datetime import datetime
from requests.exceptions import HTTPError

url = "https://smart-farm.kz:8502/api/v2/RawFeedings"
headers = {'Content-type': 'application/json'}
timen = str(datetime.now())

payload = {
            "Eventdatetime": timen,
            "EquipmentType": "test111max",
            "SerialNumber": "test111max",
            "FeedingTime": timen,
            "RFIDNumber": "animal_id",
            "WeightLambda": 20,
            "FeedWeight": 100
        }
        
def main():
    answer = 0
    try:
        answer = requests.post(url, data = json.dumps(payload), headers = headers, timeout=5)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')

    except Exception as err:
        print(f'Other error occurred: {err}')

    finally:
        if type(answer) == requests.models.Response:
            print("hi")
        else:
            print("No")


    #print(post.status_code)

main()