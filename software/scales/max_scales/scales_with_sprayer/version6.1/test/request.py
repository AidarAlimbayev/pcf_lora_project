import requests
from loguru import logger
import socket
import binascii


@logger.catch
def __request_get():  # Get data from the server
    try:
        cow_id = "FC6599A1DF00" # Это бирка
        type_scales = "scales0623v61-6-rasp" # Это серийный номер весов
        url = 'https://smart-farm.kz:8502/api/v2/Sprayings?scalesSerialNumber=' + type_scales + \
              '&animalRfidNumber=' + cow_id # Когда отправляет запрос учитывается сериый номер и бирка cow_id 
        request_get = requests.get(url, timeout=5).json()
        print(request_get)
        return request_get
    except Exception as e:
        print('request get func error')

def connect_rfid_reader():  # Connection to RFID Reader through TCP and getting cow ID in str format
    try:
        logger.debug(f'START RFID FUNCTION')
        TCP_IP = '192.168.1.250'  # chafon 5300 reader address
        TCP_PORT = 60000  # chafon 5300 port
        BUFFER_SIZE = 1024
        animal_id = "b'435400040001'"  # Id null starting variable
        animal_id_new = "b'435400040001'"
        null_id = "b'435400040001'"
        logger.debug(f'START Animal ID animal_id: {animal_id}')
        logger.debug(f'START Null id null_id : {null_id}')

        if animal_id == null_id:  # Send command to reader waiting id of animal
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
            s.send(bytearray([0x53, 0x57, 0x00, 0x06, 0xff, 0x01, 0x00, 0x00, 0x00,
                              0x50]))  # Chafon RU5300 Answer mode reading mode command
            data = s.recv(BUFFER_SIZE)
            animal_id = str(binascii.hexlify(data))
            animal_id_new = animal_id[:-5]  # Cutting the string from unnecessary information after 4 signs
            animal_id_new = animal_id_new[-12:]  # Cutting the string from unnecessary information before 24 signs
            logger.debug(f'Raw ID animal_id: {animal_id}')
            logger.debug(f'New ID animal_id_new: {animal_id_new}')
            logger.debug(f'Null id null_id : {str(null_id)}')
            s.close()
        if animal_id_new == null_id:  # Id null return(0)
            connect_rfid_reader()
        else:  # Id check return(1)
            animal_id = "b'435400040001'"
            logger.debug(f'Success step 2 RFID. animal id new: {animal_id_new}')
            return animal_id_new
    except Exception as e:
        logger.error(f'Error connect to Arduino {e}')
    else:
        logger.debug(f'2 step RFID')

def main():
    logger.info(f'If you want to know your rfid number enter 1')
    logger.info(f'if you want to take the task from server enter 2')
    z = input()
    if z == "1":
        print(connect_rfid_reader())
    else:
        __request_get()


main()