import requests
from loguru import logger
import json
@logger.catch()
def post_array_data(type_scales, animal_id, weight_list, weighing_start_time, weighing_end_time):
    #try:
        logger.debug(f'Post data function start')
        url = 'https://smart-farm.kz:8502/v2/OneTimeWeighings'
        headers =  {'Content-Type': 'application/json; charset=utf-8'}
        data = {
                "ScalesSerialNumber": type_scales,
                "WeighingStart": weighing_start_time,
                "WeighingEnd": weighing_end_time,
                "RFIDNumber": animal_id,
                "Data": weight_list
                }  
        print(f'{data}')
        post = requests.post(url, data=json.dumps(data), headers=headers, timeout=3)
        logger.debug(f'Answer from server: {post}') # Is it possible to stop on this line in the debug?
    #     logger.debug(f'Content from main server: {post.content}')
    # except Exception as e:
    #     logger.error(f'Error post data: {e}')
    # {'ScalesSerialNumber': 'scales0323v61-1', 'WeighingStart': '2023-03-18 11:19:45.081111', 
    #  'WeighingEnd': '2023-03-18 11:20:01.154629', 'RFIDNumber': '024719404d7d', 
    #  'Data': [76.45, 77.44, 78.22, 77.77, 78.12, 77.95, 78.01, 77.98, 78.03, 78.14, 77.92, 77.79, 78.03]}


def main():
    post_array_data('scales0323v61-1', '024719404d7d', [76.45, 77.44, 78.22, 77.77, 78.12, 77.95, 78.01, 77.98, 78.03, 78.14, 77.92, 77.79, 78.03],
                    '2023-03-18 11:19:45', '2023-03-18 11:20:01')
    
main()