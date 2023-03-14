import RPi.GPIO as GPIO
import time
from collections import Counter

class HX711:

    def __init__(self, dout, pd_sck, gain = 128, window = 50):
 
        self.adc_arr = []
        self.calib_arr = []
        self.window = window
        self.GAIN = gain
        self.SCALE = 1
        self.OFFSET = 0
        self.NOIZE = 0
        self.ready_counter = 0

        GPIO.setmode(GPIO.BCM)

        # Set the pin numbers
        self.PD_SCK = pd_sck
        self.DOUT = dout

        # Setup the GPIO Pin as output
        GPIO.setup(self.PD_SCK, GPIO.OUT)

        # Setup the GPIO Pin as input
        GPIO.setup(self.DOUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Power up the chip
        self.power_up()
        self.set_gain(gain)


    def set_gain(self, gain=128):
        try:
            if gain == 128:
                self.GAIN = 3
            elif gain == 64:
                self.GAIN = 2
            elif gain == 32:
                self.GAIN = 1
        except:
            self.GAIN = 3  # Sets default GAIN at 128

        GPIO.output(self.PD_SCK, False)
        self.read()


    def set_scale(self, scale):
        self.SCALE = scale


    def set_offset(self, offset):
        self.OFFSET = offset


    def get_offset(self):
        return self.OFFSET
    
    
    def get_scale(self):
        return self.SCALE
    

    def _ready(self):
        """
        Data is ready for reading when DOUT is low
        :return True if there is some date
        :rtype bool
        """

        _is_ready = GPIO.input(self.DOUT) == 0
        # print("check data ready for reading: {result}".format(
        #     result="YES" if _is_ready is True else "NO"
        # ))
        return _is_ready


    def read(self):
        """
        Read data from the HX711 chip
        :param void
        :return reading from the HX711
        """
        self.ready_counter = 0
        
        # Control if the chip is ready
        while self._ready() is False:
            self.ready_counter +=1 
            #pass
        
        #print(f'Exit from if {ready_counter}\n')
        self.NOIZE = 0
        count = 0

        for i in range(24):
            GPIO.output(self.PD_SCK, True)
            count = count << 1
            GPIO.output(self.PD_SCK, False)
            if(GPIO.input(self.DOUT)):
                count += 1
        
        GPIO.output(self.PD_SCK, True)
        count = count ^ 0x800000
        GPIO.output(self.PD_SCK, False)

        # set channel and gain factor for next reading
        for i in range(self.GAIN):
            GPIO.output(self.PD_SCK, True)
            GPIO.output(self.PD_SCK, False)

        #count = self.pre_filter(count, ready_counter)
        return count


    def pre_filter(self, count):

        if self.ready_counter == 0:
            self.NOIZE +=1
            #print(f'{self.NOIZE} if is: {ready_counter}\n\n')
            if len(self.adc_arr) > 40:
                if self.NOIZE < 40:
                    #self.reset()
                    return 9999999      

        if self.ready_counter > 100000:
            self.NOIZE +=1
            #print(f'{self.NOIZE} if is: {ready_counter}\n\n')
            if self.NOIZE < 40:
                #self.reset()
                return 9999999
        
        return count


    def get_measure(self):
        adc_val = self.read()
        adc_val = self.pre_filter(adc_val)
        
        if adc_val == 9999999:
            if len(self.adc_arr) > 1:
                self.adc_arr.pop()
                return round(sum(self.adc_arr)/len(self.adc_arr),2) 
            else:
                return 0
        
        adc_val = (adc_val-self.OFFSET)
        #print(f'Weight is {adc_val/self.SCALE}')
        return round(adc_val/self.SCALE, 2)


    def set_arr(self, arr):
        self.adc_arr = arr


    def get_arr(self):
        return self.adc_arr


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
        """
        Tare functionality fpr calibration
        :param times: set value to calculate average
        """
        sum = self.read_average(times)
        self.set_offset(sum)


    def reset(self):
        self.power_down()
        time.sleep(.0001)
        self.power_up()


    def power_down(self):
        """
        Power the chip down
        """
        GPIO.output(self.PD_SCK, False)
        GPIO.output(self.PD_SCK, True)


    def power_up(self):
        """
        Power the chip up
        """
        GPIO.output(self.PD_SCK, False)


    def read_average(self, times=16):
        """
        Calculate average value from
        :param times: measure x amount of time to get average
        """
        sum = 0
        for i in range(times):
            sum += self.read()
        return sum / times
    

    def calib_read(self, times = 20):
        """Use only in calibration"""
        for i in range(times):
            self.calib_arr.append(self.read())
        counter = Counter(self.calib_arr)
        most_common = counter.most_common(1)[0][0]
        return most_common


    def get_weight(self, times=16):
        """
        :param times: Set value to calculate average, 
        be aware that high number of times will have a 
        slower runtime speed.        
        :return float weight in grams
        """
        value = (self.read_average(times) - self.OFFSET)
        grams = (value / self.SCALE)
        return grams
