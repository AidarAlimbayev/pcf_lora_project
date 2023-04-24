import serial
from collections import Counter
import time
from collections import Counter
from loguru import logger

@logger.catch()
class ArduinoSerial:

    def __init__(self, port, baud_rate=9600, timeout = 1, window = 50):
        self.adc_arr = []
        self.calib_arr = []
        self.window = window
        self.SCALE = 1
        self.OFFSET = 0
        self.timeout = timeout
        self.NOIZE = 0
        self.port = port
        self.baud_rate = baud_rate
        self.arduino = None 


    def connect(self): # Создаение объекта serial
        self.arduino = serial.Serial(self.port, self.baud_rate, bytesize=serial.EIGHTBITS, timeout = self.timeout)
        logger.info(f'ARDUINO{self.arduino}')


    def disconnect(self):   # Удаление объекта 
        self.arduino.close()


    def set_arr(self, arr):  # задать значение массива-окна
        self.adc_arr = arr


    def get_arr(self):  # получить значение массива-окна
        return self.adc_arr


    def read_data(self): # Считывание данных с arduino
        if not self.arduino:
            raise ValueError(f'Arduino is not connected\n')
        try:
            self.arduino.write(b'\x02') # Отправка байта
            response = self.arduino.read(4) # Получение ответа
            return int.from_bytes(response, byteorder='big', signed=False) # Из байта в число
        except serial.SerialTimeoutException as e:
            print(f'Timeout error: {e}')


    def set_scale(self, scale): # Установка значения scale
        self.SCALE = scale


    def set_offset(self, offset):  # Установка значения offset (Тара)
        self.OFFSET = offset


    def get_offset(self):   # Получить 
        return self.OFFSET
    
    
    def get_scale(self):    # Получить бля
        return self.SCALE


    def get_measure(self):  # Основная функция для получения и конвертации данных с arduino. 
                            # При вызове получаем один вес
        adc_val = self.read_data()      
        adc_val = (adc_val-self.OFFSET)
        #print(f'Weight is {adc_val/self.SCALE}')
        return round(adc_val/self.SCALE, 2)


    def check_weight(self): # Тут думаю даже ёжик разберется 
        adc_val = self.get_measure()
        if adc_val < 20:
            return False
        return True
    

    def calc_mean(self):    # Смуф фильтр. 
        adc_val = self.get_measure()
        if len(self.adc_arr)==self.window:
            self.adc_arr.pop(0)
        self.adc_arr.append(adc_val)
        adc_avg = sum(self.adc_arr)/len(self.adc_arr)
        #print(f'Inside arr: {self.adc_arr}')
        return round(adc_avg, 2)


    def common_filter(self): # Фильтр для получения самого повторяющегося числа в массиве
        return Counter(self.get_arr()).most_common(1)[0][0]
    

    def tare(self, times=16):   # Это для прикола, тарирование
        sum = self.read_average(times)
        self.set_offset(sum)
        return sum/self.OFFSET


    def read_average(self, times=16): # Получение 16 измерении и вывод среднего
                                    # Не использует массив. А также, значение не 
                                    # конвертированные. Нам не нужно
        sum = 0
        for i in range(times):
            sum += self.read_data()
        return sum / times


    def calib_read(self, times = 20):  # Функция для калибровки
        """Use only in calibration"""
        self.calib_arr = []
        for i in range(times):
            self.calib_arr.append(self.read_data())
        counter = Counter(self.calib_arr)
        most_common = counter.most_common(1)[0][0]
        return most_common


    def get_weight(self, times=16):     # Точно не помню зачем написал эту функцию, 
                                        # Но она считывает 32 раза вес и выдает среднюю 
                                        # В готовом виде
        value = (self.read_average(times) - self.OFFSET)
        weight = (value / self.SCALE)
        return weight
