import array
import random
import numpy as np

adc_arr = []

window = 50 #Окно сглаживания

def calc_mean(adc_val):
    #adc_arr.pop(0)
    global adc_arr
    if len(adc_arr) == window: # Если длина массива равна окну
        adc_arr.pop(0) # удаляем первый элемент
    adc_arr.append(adc_val)
    adc_avg = sum(adc_arr)/len(adc_arr)
    if adc_avg < 100:
        adc_arr = []
    return adc_avg
    

def main():
    file = open("mean.txt", "w")
    for i in range(1):
        z = round(np.random.uniform(290.5, 295.5),2) # Имитация погрешности в +-2,5 кг
        adc_avg=calc_mean(z)
        file.write(f'{i} array of: {adc_arr}\n average of array: {adc_avg}\n\n')
    file.close()
    
        
main()