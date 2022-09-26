
from dataclasses import dataclass
from loguru import logger
import requests
import json
import values as vl
from dataclasses import dataclass
import timeit
import datetime 
from typing import NamedTuple

@dataclass
class Values(NamedTuple):
    drink_start_time: float
    spray_duration: int
    type_scales: str
    cow_id: str
    pin: int
    server_time: str
    task_id: int
    new_volume: float
    spraiyng_type: int
    volume: float

@logger.catch
def valuesdefault():
    values = Values(0, 0, '', '', 0, '', 0, 0, 0, 0)
    return values

val = valuesdefault()
print(val)

# t = timeit.default_timer()
# print(type( {'pcf_model_5': [40, 22], 'pcf_model_6': [40, 32], 'pcf_model_7': [40, 43], 'pcf_model_10': [40, 54]}))

# def check():
#     vl.values['pin'] = 40
#     vl.values['gpio_state'] = True
#     vl.values['spray_duration'] = 32



# wf = [90.4, 150.3, 185.2, 182.9, 184.26, 183.9, 210.3, 187.4, 182.5, 173.5, 67.2, 10.2]
# try:
#     logger.debug(fPost data function start)
#     print(1)
#     url = https://smart-farm.kz:8502/v2/OneTimeWeighings

#     headers =  {Content-Type: application/json; charset=utf-8}
#     info = {
#         "ScalesSerialNumber": "aidar-scales-1",
#         "WeighingStart": "2022-09-08T18:08:03.293Z",
#         "WeighingEnd": "2022-09-08T18:08:27.293Z",
#         "RFIDNumber": "391001999000001",
#         "Data": wf
#         }
#     print(4)
    
#     print(requests.head(url).headers)
#     post = requests.post(url, data=json.dumps(info), headers=headers, timeout=0.5)
#     print(5)
#     logger.debug(fAnswer from server: {post}) # Is it possible to stop on this line in the debug?
#     logger.debug(fContent from main server: {post.content})
# except Exception as e:
#     logger.error(fError post data: {e})
