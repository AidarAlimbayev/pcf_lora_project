#!/usr/bin/python3

"""File containing the main variables for automatic control of animal spraying.
Author: Suieubayev Maxat
Contact: maxat.suieubayev@gmail.com
Number: +7 775 818 48 43"""

from dataclasses import dataclass
from loguru import logger

@dataclass(frozen=True)
class Pin:
    pcf_model_5: list = 40, 22
    pcf_model_6: list = 40, 32
    pcf_model_7: list = 40, 43
    pcf_model_10: list = 40, 54


@dataclass
class Values:
    drink_start_time: float
    spray_duration: int
    type_scales: str
    cow_id: str
    pin: int
    server_time: str
    task_id: int
    new_volume: float
    spraying_type: int
    volume: float
    flag: bool

    def default(self):
        self.drink_start_time = 0
        self.spray_duration = 0
        self.type_scales = ''
        self.cow_id = ''
        self.pin = 0
        self.server_time = ''
        self.task_id = 0
        self.new_volume = 0
        self.spraying_type = 0
        self.volume = 0
        return self
