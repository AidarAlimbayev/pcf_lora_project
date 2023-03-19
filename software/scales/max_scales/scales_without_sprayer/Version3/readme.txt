Idea's author: Baiguanish Sanat
Code's author: Suieubayev Maxat

Version 3 differs from version 2 in that in this project there was a need to add Arduino. 
Reading data directly from the ADC to the raspberry introduces a new problem, namely, 
additional pulses appear, which entails noise. The pulse length also increases. 
The conclusion of using version 2 is that Python or Raspberry is not capable of reading data at the required speed.

In version 3, it was decided to add Arduino. The main task of the arduino is 
to read data from the ADC and transfer it to the raspberry without converting.
Most of version 2 should go unchanged to version 3. The main difference 
should be the process of processing the data coming from Arduino and 
converting the incoming number into weight.

Adс_data class created. An example of using a class:
import adc_data
port = '/dev/ttyUSB0'
            offset,scale=Calibration()
obj = adc_data.ArduinoSerial(port)
obj.set_scale(scale)
obj.set_offset(offset)
raw = obj.read_data()
weight1 = obj.get_measure() # 1 ready weight
weight32 = obj.get_weight() # 32 numbers average 
weight_smooth = obj.calc_mean() # smooth filter 

https://habr.com/ru/post/134375/ here you can find example of smmoth filter

Version3 directories map:
software/main/max_scales/

