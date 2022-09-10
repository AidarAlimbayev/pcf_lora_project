from asyncio import new_event_loop
from datetime import datetime
import timeit
import time 

sclales_list = { 'pcf_model_5': [40, 22],
                 'pcf_model_6': [40, 32],
                 'pcf_model_7': [40, 43],
                 'pcf_model_10': [40, 54]
                }

#spray_get_url: 'https://smart-farm.kz:8502/api/v2/Sprayings?scalesSerialNumbe:'+type_scales+'&animalRfidNumbe:'+cow_id
values = {  'gpio_state': False,
            'weight_list': [],
            'start_timedate': str(datetime.now()),
            'drink_start_time': timeit.default_timer(),
            'spray_duration': 0,
            'type_scales': 'pcf_1_model_1_80',
            'cow_id': '010117406415',
            'pin': 0,
            'start_time': 0,
            'server_time': '',
            'task_id': 0,
            'new_volume': 0,
            'spraiyng_type': 0,
            'position': False,
            'volume': 0}


