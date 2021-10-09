#raw_data_processing.py

import pсflib as pl

type_scales = 'A'

def main():

    # Арсений: здесь считывание с БД raw_data(cow_id, weight, timestamp)
    # Может быть в класс все положить, будем ООП делать?
    # Адиль: лог о статусе считывания данных

    # Санат: нужно теперь продумать как их обрабатывать твои идеи 
    # Часть алгоритма под названием "Статистика"
    # выложить в переменные для Арсения

    # Арсений: здесь запись данных в БД cow 
    # передаваемые параметры processed_data_(cow_id, weight, timestamp)

    pl.Send_data_to_server(cow_id, weight, type_scales)

main()

