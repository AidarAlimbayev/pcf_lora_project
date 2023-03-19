#!/usr/bin/sudo python

"""Scales main file without sprayer. Version 5.1
by Alimbayev Aidar and Suieubayev Maxat."""

import _headers as hdr

requirement_list = ['loguru', 'requests', 'RPi.GPIO', 'pyserial']
hdr.install_packages(requirement_list)

import adc_data as ADC
import lib_test as pcf
import time
#time.sleep(10)
from datetime import datetime, time
from loguru import logger
import _config as cfg
import time

import matplotlib.pyplot as plt
import pandas as pd


logger.add('log/scales_{time}.log', format="{time} {level} {message}", 
level="DEBUG", rotation="1 day", compression="zip")             #serialize="True")

type_scales = cfg.get_setting("Parameters", "feeder_type")
logger.info(f'main: Test script')
title = 'Test.'

@logger.catch()
def weight_time_graph(df):
    try:
        global title
        fig, axs = plt.subplots(nrows= 4 , ncols= 1)
        fig.suptitle(title)
        fig. tight_layout (h_pad= 2)
        
        axs[0].plot(df.index, df['Weight'], 'royalblue')
        axs[0].set_title('Weight')
        axs[0].set_facecolor('azure')
        axs[0].grid(linestyle='--', linewidth=1, color = 'slategrey') 
        axs[1].plot(df.index, df['Average'], 'coral')
        axs[1].set_title('Average')
        axs[1].set_facecolor('lightblue')
        axs[1].grid(linestyle='--', linewidth=1, color = 'slategrey')
        axs[2].plot(df.index, df['Commons'], 'black')
        axs[2].set_title('Common')
        axs[2].set_facecolor('lightblue')
        axs[2].grid(linestyle='--', linewidth=1, color = 'slategrey')
        axs[3].plot(df.index, df['Execution time'], 'deeppink')
        axs[3].set_title('Execution time')
        axs[3].grid(linestyle = ':')

        # график всё в одном
        #plt.plot(df.index, df['Weight'], 'r')
        #plt.plot(df.index, df['Average'], 'b')
        #plt.plot(df.index, df['Execution time'], 'r')
        #print(list(df.columns))
        
        plt.savefig(f'docs/{title}.pdf')
        plt.show()

    except Exception as e:
        logger.error(f'Error: {e}')


@logger.catch
def main():
        logger.debug(f'Enter number of test >')
        title_num = input()
        df = pd.DataFrame(columns=['Weight', 'Average', 'Length of array', 'Commons', 'Execution time'])
        logger.debug(f'Start main script')
        port = cfg.get_setting("Parameters", "arduino_port")
        arr = []
        #pcf.calibrate()
        arduino = ADC.ArduinoSerial(port)
        arduino.connect()
        offset, scale = float(cfg.get_setting("Calibration", "offset")), float(cfg.get_setting("Calibration", "scale"))
        arduino.set_offset(offset)
        arduino.set_scale(scale)
        time.sleep(0.5)
        i = 0
        while(True):
            try:
                # logger.debug(f'Enter 1 to take adc value from arduino\n Enter 2 to exit')
                # choice = input()
                # if choice == 1:
                start_time = datetime.now().timestamp()
                moment_weight = arduino.get_measure()
                exe_time = round(datetime.now().timestamp() - start_time, 4)
                smooth_filter = arduino.calc_mean()
                common_fiter = arduino.common_filter()
                logger.info(f'Get measure funct: {moment_weight}')
                logger.info(f'Calc_mean funct: {smooth_filter}')
                logger.info(f'Common filter: {common_fiter}')
                #logger.info(f'measure_weight(): {pcf.measure_weight(arduino)}')
                logger.info(f'Array of numbers: {arduino.get_arr()}')
                if i > 5:
                    df.loc[i] = {'Weight': moment_weight, 'Average': smooth_filter, 
                                'Length of array': len(arduino.get_arr()), 
                                'Commons': common_fiter, 'Execution time': exe_time}
                i+=1
                #print(f'Not converted data: {arduino.read_data()}')
                #print(f'Most common number is: {arduino.calib_read()}')
                #print(f'Tare is: {arduino.tare()}')
                    #print(pcf.get_val(port, arr))
                    #pcf.get_one_value(port)
                    #print(pcf.get_val_class(arduino))
                # else: 
                #     break
            except KeyboardInterrupt as k:
                global title
                title = title + str(title_num)
                df.to_excel(f'docs/{title}.xlsx')
                #df.to_csv("docs/weightnings.csv")
                weight_time_graph(df)
                arduino.disconnect()
                logger.error(f'Error: {k}')
                

main()