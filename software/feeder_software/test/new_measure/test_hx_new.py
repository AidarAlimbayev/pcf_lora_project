#!/usr/bin/sudo python3
import _headers as hdr

requirement_list = ['loguru', 'requests', 'RPi.GPIO', 'numpy', 'pandas', 'matplotlib']
hdr.install_packages(requirement_list)

import new_class as HX
import _config as cfg
from loguru import logger
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO 
from collections import Counter
import sys
    
title = 'Test.'

def calibrate():
    try:
        logger.info('Start calibrate function')

        GPIO.setmode(GPIO.BCM)  
        hx = HX.HX711(21,20)
        input("Remove any items from scale. Press any key when ready.")
        offset = hx.read_average()
        logger.info("Value at zero (offset): {}".format(offset))
        hx.set_offset(offset)

        logger.info("Please place an item of known weight on the scale.")
        input("Press any key to continue when ready.")
        measured_weight = (hx.read_average()-hx.get_offset())
        item_weight = input("Please enter the item's weight in kg.\n>")
        scale = int(measured_weight)/int(item_weight)
        hx.set_scale(scale)
        logger.info(f"Scale adjusted for kilograms: {scale}")
        logger.info(f'Offset: {offset}, set_scale(scale): {scale}')

        GPIO.cleanup()
        cfg.update_setting("Calibration", "Offset", offset)
        cfg.update_setting("Calibration", "Scale", scale)
        return offset, scale
    except:
        logger.error(f'calibrate Fail')

def cleanAndExit():
    logger.info("Cleaning up...")
    GPIO.cleanup()
    logger.info("Bye!")
    sys.exit()

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

@logger.catch()
def main():
    try:
        title_num = input("Enter number of test")
        df = pd.DataFrame(columns=['Weight', 'Average', 'Length of array', 'Commons', 'Execution time'])
        
        logger.info(f'Hi! It is measure test file.\n For first you should to make a choice:')
        logger.info(f'1. Make calibration\n 2. Start measure.')
        logger.info(f'If you use this sketch first time please make calibration\n to save needed values.\n')
        choice = input()
        int_choice = int(choice)
        if int_choice == 1:
            logger.info(f'Start calibration')
            calibrate()
        logger.info(f'Calibration ended')
        GPIO.setmode(GPIO.BCM) 
        hx = HX.HX711(21,20)
        offset = float(cfg.get_setting("Calibration", "Offset"))
        scale = float(cfg.get_setting("Calibration", "Scale"))
        hx.set_scale(scale)
        hx.set_offset(offset)
        hx.reset()
        i = 0
        while True:
            #if hx.check_weight():
            #while hx.check_weight():
            start_time = datetime.now().timestamp()
            weight, length, answer = hx.calc_mean()
            exe_time = round(datetime.now().timestamp() - start_time, 4)
            adc_arr = hx.get_arr()
            counter = Counter(adc_arr)
            most_common = counter.most_common(1)[0][0]
            if i > 5:
                df.loc[i] = {'Weight': weight, 'Average': answer, 'Length of array': length, 
                            'Commons': most_common, 'Execution time': exe_time}
            print(f'Average: {answer}\n')
            #hx.reset()
            i+=1
            # hx.check_weight()
            #else:
                #hx.set_arr([])
                #hx.reset()

    except KeyboardInterrupt as k:
        global title
        title = title + str(title_num)
        df.to_excel(f'docs/{title}.xlsx')
        #df.to_csv("docs/weightnings.csv")
        weight_time_graph(df)
        logger.error(f'Error: {k}')
        cleanAndExit()
    
    except Exception as e:
        logger.error(f'Error: {e}')
        cleanAndExit()
    

main()