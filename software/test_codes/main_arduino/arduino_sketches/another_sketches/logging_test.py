###logging_test

#log_with_config.py

import logging
import logging.config
import otherMod2

def main():
    """
    Based on http://docs.python.org/howto/logging.html#configuring-logging
    """

    dictLogConfig = {
        "version":1,
        "handlers":{
            "fileHandler":{
            "class": "logging.FileHandler",
            "formatter":"myFormatter",
            "filename":"config2.log"
            }
        },
        "loggers":{
            "exampleApp":{
                "handlers":["fileHandler"],
                "level":"INFO",
                }
        },
        "formatters":{
            "myFormatter":{
                "format":"%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        }
    }

    logging.config.dictConfig(dictLogConfig)
    logger = logging.getLogger("exampleApp")
    logger.info("Program started")
    result = otherMod2.add(22, 33)
    logger.info("Done!")

if __name__ == "__main__":
    main()

# log_with_config.py
# import logging
# import logging.config
# import otherMod2
 
# def main():
#     """
#     Based on http://docs.python.org/howto/logging.html#configuring-logging
#     """
#     logging.config.fileConfig('logging.config')
#     logger = logging.getLogger("exampleApp")
    
#     logger.info("Program started")
#     result = otherMod2.add(7, 8)
#     logger.info("Done!")
 
# if __name__ == "__main__":
#     main()


# import logging
# import otherMod
# import datetime

# def main():
#     """
#     The main entry point of the application
#     """

#     logging.basicConfig(filename = "mySnake.log", level = logging.INFO)
#     logging.info("Program started")
#     #logging.info(datetime.datetime.today())
#     logging.info(datetime.datetime.now())
#     result = otherMod.add(7,8)
#     logging.info("Done!")

# if __name__ == "__main__":
#     main()

# import logging

# logging.basicConfig(filename = "sample.log", level = logging.INFO)
# log = logging.getLogger("ex")

# try:
#     raise RuntimeError
# except RuntimeError:
#     log.exception("Error!")



# #add filemode="w" to overwrite
# logging.basicConfig(filename = "sample.log", level = logging.INFO)

# logging.debug('This is a debug message')
# logging.info('Information message')
# logging.error('An error has happened')












# import logging

# logging.basicConfig(level = logging.WARNING)

# logger1 = logging.getLogger('package1.module1')
# logger2 = logging.getLogger('package2.module2')

# logger1.warning('This message comes from one module')
# logger2.warning('And this message vomes from another module')


# import logging
# import sys

# LEVELS = {'debug': logging.DEBUG,
#             'info': logging.INFO,
#             'warning': logging.WARNING,
#             'error': logging.ERROR,
#             'critical': logging.CRITICAL}

# if len(sys.argv) > 1:
#     level_name = sys.argv[1]
#     level = LEVELS.get(level_name, logging.NOTSET)
#     logging.basicConfig(level = level)

# logging.debug('This is a debug message')
# logging.info('This is a info message')
# logging.warning('This is a warning message')
# logging.error('This is a error message')
# logging.critical('This is a crirtical message')



# import glob
# import logging
# import logging.handlers

# # LOG_FILENAME = 'example.log'
# # logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
# # logging.debug('This message should go to the log file')

# LOG_FILENAME = 'logging_rotatingfile_example.out'

# #Set up a specigfc logger with our desired output level
# my_logger = logging.getLogger('MyLogger')
# my_logger.setLevel(logging.DEBUG)

# #Add the log message handler to the logger
# handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes = 20, backupCount = 5)

# my_logger.addHandler(handler)

# #Log some message

# for i in range(20):
#     my_logger.debug('i = %d' % i)

# #See what files are created
# logfiles = glob.glob('%s*' % LOG_FILENAME)

# for filename in logfiles:
#     print (filename)

