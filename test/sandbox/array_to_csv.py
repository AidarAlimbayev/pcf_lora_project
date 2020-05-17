# import pandas as pd

# list1 = ['1', '2', '3']
# list2 = ['a', 'b', 'c']
# list3 = ['x', 'y', 'z']

# frame = pd.DataFrame([list1,list2,list3]) # собираем фрейм
# frame.to_csv('my_csv_export.csv',index=False) #экспортируем в файл

import csv
import main_pcf_lib as pcf

s = pcf.serial.Serial('/dev/ttyACM0',9600)


def main():
    pcf.Connect_ARD_get_weight

if __name__=='__main__':
    main()