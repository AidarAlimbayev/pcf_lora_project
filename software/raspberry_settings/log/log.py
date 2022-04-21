from datetime import datetime, date, time
import json
import requests

animal_id = max
weight_finall = 300
type_scales = 1

try:
    url = 'http://194.4.56.86:8501/api/weights'
    headers = {'Content-type': 'application/json'}
    data = {"AnimalNumber" : "animal_id",
            "Date" : "str(datetime.now())",
            "Weight" : "weight_finall",
            "ScalesModel" : "type_scales"}
    answer = requests.post(url, data=json.dumps(data), headers=headers)
    
except Exception as e:
    print("Error send data to server", e)
else:
    print("4 step send data")