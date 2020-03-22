#logging_webdev.py

import logging

#Create a custom 
logger = logging.getLogger(__name__)




name = 'Belka'
cow_id = 15365

logger = logging.getLogger('test_logger_pcf')
logging.basicConfig(level = logging.DEBUG, filename = "webdev.log", format = '%(process)d - %(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

logger.debug('This is a debug message')
logger.info(f'{name} catched to log with ID: {cow_id}')
logger.warning('This is a warning message')


a = 5
b = 0

try: 
    c = a / b
except Exception as e:
    c = 0
    print(c)
    logger.exception("Exception occured")


logging.critical('This is a critical message')

