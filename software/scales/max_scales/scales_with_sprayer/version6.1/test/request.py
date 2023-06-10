import requests
from loguru import logger

@logger.catch
def __request_get():  # Get data from the server
    try:
        cow_id = "40103003d496"
        type_scales = "scales0406v61-2-spr"
        url = 'https://smart-farm.kz:8502/api/v2/Sprayings?scalesSerialNumber=' + type_scales + \
              '&animalRfidNumber=' + cow_id
        request_get = requests.get(url, timeout=5).json()
        print(request_get)
        return request_get
    except Exception as e:
        print('request get func error')


__request_get()