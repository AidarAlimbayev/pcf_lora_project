from asyncio.windows_events import NULL
from datetime import datetime, date, time
import logging
import os
import inspect

from numpy import void


logging.basicConfig(filename = 'print_log_test.log', level = logging.DEBUG, format='[%(filename)s:%(lineno)s - %(funcName)20s() ] %(asctime)s %(message)s')

# logger = logging.getLogger(__name__)
# FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
# logging.basicConfig(filename = 'print_log_test.log', format=FORMAT)
# logger.setLevel(logging.DEBUG)


weight_array = []
weight_null = NULL

if weight_array != [] and weight_null == NULL:
    print(-11)


bval = weight_array == weight_null

print(bval)


def print_log(message = NULL, value = NULL):
    logging.info(message)
    logging.info(value)
    #logger.debug(message)
    print(message)
    print(print_log.__name__, value)

def some_function():
    print_log("third message", 333)


some_function()