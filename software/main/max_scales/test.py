from loguru import logger
import requests
import json


wf = [90.4, 150.3, 185.2, 182.9, 184.26, 183.9, 210.3, 187.4, 182.5, 173.5, 67.2, 10.2]
try:
    logger.debug(f'Post data function start')
    print(1)
    url = 'https://smart-farm.kz:8502/v2/OneTimeWeighings'

    headers =  {'Content-Type': 'application/json; charset=utf-8'}
    info = {
        "ScalesSerialNumber": "aidar-scales-1",
        "WeighingStart": "2022-09-08T18:08:03.293Z",
        "WeighingEnd": "2022-09-08T18:08:27.293Z",
        "RFIDNumber": "391001999000001",
        "Data": wf
        }
    print(4)
    
    print(requests.head(url).headers)
    post = requests.post(url, data=json.dumps(info), headers=headers, timeout=0.5)
    print(5)
    logger.debug(f'Answer from server: {post}') # Is it possible to stop on this line in the debug?
    logger.debug(f'Content from main server: {post.content}')
except Exception as e:
    logger.error(f'Error post data: {e}')
