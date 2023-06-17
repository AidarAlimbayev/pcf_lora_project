
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

Version6.1 directories map:
software/scales/max_scales/Version3:
    - arduino/SerialCallResponse_RPi.ino it's a main arduino sketch.
Response HX711_data to Raspberry.
    - arduino/HX711-master.zip HX711 library
    - version3_test/test_v3.py testing arduino-rasp communication protocol
    - adc_data.py - new_class which creates connectcion between arduino
and raspberry, receives and converts data, deletes communication and etc.
    - lib_test.py - module, contains main functions
    - _config.py - config.ini manager
    - _headers.py - pip and import manager
    - pcf.service - daemon file
    - config.ini - contains main parameters

************************************************************
Installing manual: 

1. Create directory scales6.1. Path: /home/pi/scales6.1
2. cd scales6.1
3. Move next files to scales6.1:    *_config.py
                                    *_headers.py
                                    *adc_data.py
                                    *config.ini
                                    *lib_test.py
                                    *main_pcf.py
                                    *pcf.service
4. Open config.ini (sudo nano config.ini)
5. Change next fields: {*model 
                        *type
                        *serial_number} 
parameters can be found at the link:
https://docs.google.com/spreadsheets/d/1XeYxa0_bUGq_OvfEMQHy445ZObuPY38OtOF7z158Gro/edit#gid=0

                        *arduino_port - 
If arduino is not connected, connect it first, then 
in terminal enter command: ls /dev/tty* 
if everything is normal you can find one of this ports 
{ttyUSB0, ttyUSB1, ttyACM0, ttyACM1}. For example ttyACM0:
arduino_port = /dev/ttyACM0

6. Start main code: python3 main_pcf.py
7. For first time, you should make Calibration. In 5 seconds after start main_pcf
enter "1" and follow the instruction. After Calibration end enter ctrl+c

Example:
2023-03-18T14:38:25.537303+0600 INFO ("[1] to calibrate
" "[2] to start measure
>")

8. in terminal cp /home/pi/scales6.1/pcf.service /etc/systemd/system/
9. sudo systemctl start pcf.service
10. sudo systemctl enable pcf.service
11. sudo systemctl status pcf.service 

Example of normal status:
● pcf.service - pcf.service Service
     Loaded: loaded (/etc/systemd/system/pcf.service; enabled; vendor preset: e>
     Active: active (running) since Sat 2023-03-18 14:38:21 +06; 20h ago
   Main PID: 563 (python3)
      Tasks: 1 (limit: 3720)
        CPU: 2.857s
     CGroup: /system.slice/pcf.service
             └─563 /usr/bin/python3 /home/pi/scales6.1/main_pcf.py


***********************************************************
Testing manual: 
1. python3 main_pcf.py
2. wait about 5 seconds
3. starting 
4. for first, scales are waiting rfid label
2023-03-18T14:38:48.177496+0600 DEBUG Success step 2 RFID. animal id new: 003818105d01
5. scales should start collect the weights: 
2023-03-18T14:48:34.506062+0600 DEBUG Common filter weights: [85.76]
2023-03-18T14:48:35.677266+0600 DEBUG Common filter weights: [85.76, 85.88]
2023-03-18T14:48:36.848694+0600 DEBUG Common filter weights: [85.76, 85.88, 85.83]
2023-03-18T14:48:38.020152+0600 DEBUG Common filter weights: [85.76, 85.88, 85.83, 85.72]
2023-03-18T14:48:39.191563+0600 DEBUG Common filter weights: [85.76, 85.88, 85.83, 85.72, 85.77]
2023-03-18T14:48:40.363015+0600 DEBUG Common filter weights: [85.76, 85.88, 85.83, 85.72, 85.77, 85.74]
2023-03-18T14:48:41.534429+0600 DEBUG Common filter weights: [85.76, 85.88, 85.83, 85.72, 85.77, 85.74, 85.64]
2023-03-18T14:48:42.705766+0600 DEBUG Common filter weights: [85.76, 85.88, 85.83, 85.72, 85.77, 85.74, 85.64, 99.48]
6. Get off the scales 
7. Response should return 200:
2023-03-18T14:48:43.248949+0600 DEBUG Post data function start
2023-03-18T14:48:43.546386+0600 DEBUG Answer from server: <Response [200]>
2023-03-18T14:48:43.548329+0600 DEBUG Content from main server: b'1042'
2023-03-18T14:48:43.549307+0600 DEBUG START SEND DATA TO SERVER:
2023-03-18T14:48:43.685788+0600 DEBUG Answer from server: <Response [200]>
2023-03-18T14:48:43.686849+0600 DEBUG Content from main server: b'146761'

follow the link https://smart-farm.kz:8500/Login.aspx?ReturnUrl=%2fDefault.aspx
user admin
password 12qwaszx
Оборудование/smart-весы/Разовое взвешивание
If table data is updated by your's test data everything is good.
Done.

***********************************************************
Troubleshooting:

-Arduino error - arduino is not connected or wrong port /dev/tty*
-Response <any number except 200> - maybe problem at server side
-Not collecting weights - calibration ended wrong. Wrong offset or scale value