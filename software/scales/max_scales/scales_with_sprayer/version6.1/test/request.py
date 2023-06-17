import requests
from loguru import logger

@logger.catch
def __request_get():  # Get data from the server
    try:
        cow_id = "111test111" # Это бирка
        type_scales = "maxtestscalesdelete17.06" # Это серийный номер весов
        url = 'https://smart-farm.kz:8502/api/v2/Sprayings?scalesSerialNumber=' + type_scales + \
              '&animalRfidNumber=' + cow_id # Когда отправляет запрос учитывается сериый номер и бирка cow_id 
        request_get = requests.get(url, timeout=5).json()
        print(request_get)
        return request_get
    except Exception as e:
        print('request get func error')


__request_get()