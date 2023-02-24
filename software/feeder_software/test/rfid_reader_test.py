from loguru import logger
import socket
import binascii

logger.add('rfid_reader_test.log', format="{time} {level} {message}", 
level="DEBUG", rotation="1 day", compression="zip")  

def __connect_rfid_reader():                                      # Connection to RFID Reader through TCP and getting cow ID in str format
    try:    
        logger.info(f'Start connect RFID function')
        TCP_IP = '192.168.1.250'                                #chafon 5300 reader address
        TCP_PORT = 60000                                        #chafon 5300 port
        BUFFER_SIZE = 1024
        animal_id = "b'435400040001'"                           # Id null starting variable
        animal_id_new = "b'435400040001'"
        null_id = "b'435400040001'"

        if animal_id == null_id: # Send command to reader waiting id of animal
            logger.info(f' In the begin: Animal ID: {animal_id}')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
            s.send(bytearray([0x53, 0x57, 0x00, 0x06, 0xff, 0x01, 0x00, 0x00, 0x00, 0x50])) #Chafon RU5300 Answer mode reading mode command
            data = s.recv(BUFFER_SIZE)
            animal_id= str(binascii.hexlify(data))
            animal_id_new = animal_id[:-5] #Cutting the string from unnecessary information after 4 signs 
            animal_id_new = animal_id_new[-12:] #Cutting the string from unnecessary information before 24 signs
            logger.info(f'After end: Animal ID: {animal_id}')
            s.close()             
        if animal_id_new == null_id: # Id null return(0)
            __connect_rfid_reader()
        else: # Id checkt return(1)
            animal_id = "b'435400040001'"

            return animal_id_new
    except Exception as e:
        logger.error(f'Error connect RFID reader {e}')


def main():
    try:
        logger.info(f'Start test rfid reader antenna\n')
        cow_id = '435400040001'
        while(1):
            cow_id = __connect_rfid_reader()
            if cow_id != '435400040001':
                logger.info(f'Cow_id now is: {cow_id}\n')
    except TypeError as e:
        logger.error(f'Error {e}')

main()