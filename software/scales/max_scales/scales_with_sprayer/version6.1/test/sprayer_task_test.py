from loguru import logger
from datetime import datetime
import requests


def sprayer_task_request(cow_id):

    current_time = datetime.utcnow()

    formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    logger.debug(f"Start spray_json_payload function")
    data = {
            "EventDate": formatted_time,
            "TaskId": 'values.task_id',
            "ScalesSerialNumber": 'values.type_scales',
            "SpayerSerialNumber": "s01000001",
            "RFIDNumber": 'values.cow_id',
            "SprayingType":' values.spraying_type',
            "Volume": 'values.new_volume'
        }
    
def __request_get(cow_id, type_scales):  
    try:
        url = 'https://smart-farm.kz:8502/api/v2/Sprayings?scalesSerialNumber=' + type_scales + \
              '&animalRfidNumber=' + cow_id
        request_get = requests.get(url, timeout=5).json()
        return request_get
    except Exception as e:
        logger.error(f'request get func error {e}')

    
def main():
    cow_id = 'FC6599A1DF00'
    type_scales = 'Velvet_FC6599A1DF00'
    #sprayer_task_request(cow_id)
    request_get_json = __request_get(cow_id, type_scales)
    logger.debug(f'JSON Request: {request_get_json}')
    
main()