#logging_webdev.py

import logging
import logging_webdev.config
logging.config.fileConfig(fname='logging_webdev.config', disable_existing_loggers=False)

# Get the logger specified in the file
logger = logging.getLogger(__name__)
logger.debug('This is a debug message')

# import logging

# #Create a custom logger 
# logger = logging.getLogger(__name__)

# #Create handlers
# c_handler = logging.StreamHandler()
# f_handler = logging.FileHandler('webdev.log')
# c_handler.setLevel(logging.WARNING)
# f_handler.setLevel(logging.ERROR)

# #Create formatters and add it to handlers
# c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
# f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# c_handler.setFormatter(c_format)
# f_handler.setFormatter(f_format)

# #Add handlers to the logger
# logger.addHandler(c_handler)
# logger.addHandler(f_handler)

# logger.warning('This is a warning')
# logger.error('This is an error')



# name = 'Belka'
# cow_id = 15365

# logger = logging.getLogger('test_logger_pcf')
# logging.basicConfig(level = logging.DEBUG, filename = "webdev.log", format = '%(process)d - %(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

# logger.debug('This is a debug message')
# logger.info(f'{name} catched to log with ID: {cow_id}')
# logger.warning('This is a warning message')


# a = 5
# b = 0

# try: 
#     c = a / b
# except Exception as e:
#     c = 0
#     print(c)
#     logger.exception("Exception occured")


# logging.critical('This is a critical message')

