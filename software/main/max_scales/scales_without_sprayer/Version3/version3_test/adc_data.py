import serial
import time
from collections import Counter

class ArduinoSerial:

    def __init__(self, port, baud_rate, timeout = 1, window = 50):
 
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

    def connect(self):
        self.arduino = serial.Serial(self.port, self.baud_rate, self.timeout)

    def disconnect(self):
        if self.arduino:
            self.arduino.close()

    def set_arr(self, arr):
        self.adc_arr = arr


    def get_arr(self):
        return self.adc_arr

    def read_data(self):
        if not self.arduino:
            raise ValueError(f'Arduino is not connected\n')
        try:
            self.arduino.write(b'\x02')
            response = self.arduino.read(4)
            return int.from_bytes(response, byteorder='big', signed=False)
        except serial.SerialTimeoutException as e:
            print(f'Timeout error: {e}')


    def set_scale(self, scale):
        self.SCALE = scale


    def set_offset(self, offset):
        self.OFFSET = offset


    def get_offset(self):
        return self.OFFSET
    
    
    def get_scale(self):
        return self.SCALE


    def get_measure(self):
        adc_val = self.read_data()
        
        if adc_val == 9999999:
            if len(self.adc_arr) > 1:
                self.adc_arr.pop()
                return round(sum(self.adc_arr)/len(self.adc_arr),2) 
            else:
                return 0
        
        adc_val = (adc_val-self.OFFSET)
        #print(f'Weight is {adc_val/self.SCALE}')
        return round(adc_val/self.SCALE, 2)


    def check_weight(self):
        adc_val = self.get_measure()
        if adc_val < 20:
            return False
        return True
    

    def calc_mean(self):
        adc_val = self.get_measure()
        if len(self.adc_arr) == 0:
            self.adc_arr.append(adc_val)
        if len(self.adc_arr)==self.window:
            self.adc_arr.pop(0)
        self.adc_arr.append(adc_val)
        adc_avg = sum(self.adc_arr)/len(self.adc_arr)
        #print(f'Inside arr: {self.adc_arr}')
        return round(adc_avg, 2)


    def calc_mean_filter(self):
        adc_val = self.get_measure()
        if len(self.adc_arr)==self.window:
            self.adc_arr.pop(0)
            adc_avg = sum(self.adc_arr)/len(self.adc_arr)
            if adc_avg - 10 < adc_val < adc_avg + 10:
                self.adc_arr.append(adc_val)
                adc_avg = sum(self.adc_arr)/len(self.adc_arr)
                print(f'Inside arr: {self.adc_arr}')
        else:
            self.adc_arr.append(adc_val)
        print(f'Inside arr: {self.adc_arr}')
        adc_avg = sum(self.adc_arr)/len(self.adc_arr)
        
        return round(adc_val,2), len(self.adc_arr), round(adc_avg, 2)
        #return round(adc_avg, 2)
    

    def tare(self, times=16):
        sum = self.read_average(times)
        self.set_offset(sum)


    def read_average(self, times=16):

        sum = 0
        for i in range(times):
            sum += self.read_data()
        return sum / times
    

    def calib_read(self, times = 20):
        """Use only in calibration"""
        self.calib_arr = []
        for i in range(times):
            self.calib_arr.append(self.read_data())
        counter = Counter(self.calib_arr)
        most_common = counter.most_common(1)[0][0]
        return most_common


    def get_weight(self, times=16):

        value = (self.read_average(times) - self.OFFSET)
        weight = (value / self.SCALE)
        return weight
