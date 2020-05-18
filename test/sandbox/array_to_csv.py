# import pandas as pd

# list1 = ['1', '2', '3']
# list2 = ['a', 'b', 'c']
# list3 = ['x', 'y', 'z']

# frame = pd.DataFrame([list1,list2,list3]) # собираем фрейм
# frame.to_csv('my_csv_export.csv',index=False) #экспортируем в файл

import csv
import serial
import binascii
import re
import pandas as pd

s = serial.Serial('/dev/ttyACM0',9600)

def connect_to_ard():
        weight = (str(s.readline()))
        weight_new = re.sub("b|'|\r|\n", "", weight[:-5])
        print(weight_new)

        weight_list = []
        mid_weight = 0
        while (float(weight_new) != 0): # Collecting weight to array 
            weight = (str(s.readline()))
            print("Weight :", weight)
            weight_new = re.sub("b|'|\r|\n", "", weight[:-5])
            print("Substracted weight: ", weight_new)
            #float(weight_new)
            # Часть кода для сохранения всех значений веса в CSV файл сырых данных
            # with open('eggs.csv', 'w', newline='') as csvfile:
            #     wr = csv.writer(csvfile)
            #     print(type(weight_new))
            #     wr.writerow(weight_new)

            weight_list.append(float(weight_new))
        if weight_list == 0 or weight_list == []:
            return(0)
        else:
            if weight_list != 0:
                del weight_list[-1]
            weight_finall =  sum(weight_list) / len(weight_list) 

            # Часть кода для записи массива в CSV файл сырых данных
            cow_id = 1111
            sep_line = "__________"
            with open('eggs.csv', 'a+', newline='') as csvfile:
                wtr = csv.writer(csvfile)
                wtr.writerow([sep_line])
                wtr.writerow([cow_id])
                for x in weight_list : wtr.writerow ([x])
                csvfile.close()
            # конец части кода записи сырых данных
            
            weight_list = []
            return(float(weight_new))


def main():
    #pcf.Connect_ARD_get_weight
    weight = connect_to_ard()
    print(weight)
        

if __name__=='__main__':
    main()