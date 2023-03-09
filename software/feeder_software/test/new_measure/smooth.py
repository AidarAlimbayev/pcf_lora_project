import numpy as np

def smooth(input, n, window):   # передаем массив чисел, длину массива и окно - середина массива 
    try:
        output = np.zeros(n)        # создаем выходной массив рамзмером int n и заполняем нулями
        if window % 2 == 0:         # если массив чётный 
            window += 1             # добавляем 1 для симметрии
        hw = (window - 1) // 2      # размах окна влево и вправо ????? 
        output[0] = input[0]        # первый элемент берем как есть

        for i in range(1, n):       # цикл от 1 до n-1, исключаем первый элемент массива
            tmp = 0                 # объявляем tmp
            if i < hw:              # если i в первой половине окна
                k1 = 0              # то что равно здесь
                k2 = 2 * i          # то что равно здесь
                z = k2 + 1          # и то что здесь передаём в следующий цикл for
            elif (i + hw) > (n - 1):    # если i во второй половине окна
                k1 = i - n + i + 1  
                k2 = n - 1          
                z = k2 - k1 + 1     # и то что здесь передаём в следующий цикл for
            else:                   # если i в середине окна
                k1 = i - hw
                k2 = i + hw
                z = window          # и то что здесь передаём в следующий цикл for

            for j in range(k1, k2+1): # цикл от к1 до к2 
                tmp += input[j]      # проходим по всем элементам input с учетом окна 
            output[i] = tmp / z     # записываем среднее значение элементов окна
        return output
    except ValueError as e:
        print(f'Error: {e}')


def measurement(input=0):
    try:
        for i in range(len(input)):
            input[i] = round(input[i],2)

        n = len(input)
        window = 5
        output = smooth(input, n, window)
        return input, output
    except Exception as e:
        print(f'Error: {e}')


import timeit

def calculating(input, file, z, str):
    try:
        sm = timeit.default_timer()
        input, out = measurement(input)
        em = timeit.default_timer()
        sa = timeit.default_timer()
        avi = sum(input)/len(input)
        avo = sum(out)/len(out)
        ea = timeit.default_timer()
        file.write(f'\t{z} test description: \n')
        file.write(f'\tFunction execution time: {em - sm}\n')
        file.write(str)
        file.write((f'input[{z}] is {input}\n\n'))
        file.write(f'output[{z}] is {out}\n\n"""')
        file.write(f'\n\tInput arrays lenght: {len(input)}\n\tOutput arrays lenght: {len(out)}\n')
        file.write(f'\tAverage execution time: {ea - sa}\n')
        file.write(f'\tAverage of input is: {round(avi,2)}\n')
        file.write(f'\tAverage of output is: {round(avo,2)}\n\n\n')
    except ValueError as v:
        print(f'Error: {v}')

def main():
    try:
        file = open("smooth_test_report.txt", "w")
        file.write(f'\t\t\t\tSMOOTH FUNCTION TEST\n\n\n')
        
        in1 = np.random.rand(100) 
        str1 = f'\tfloat[100] numbers with range(0, 1):"""\n\n'
        calculating(in1, file, 1, str1)

        in2 = np.random.uniform(10, 100, 100)
        str2 = f'\tfloat[100] numbers with range(10, 100):"""\n\n'
        calculating(in2, file, 2, str2)

        in3 = np.random.uniform(290.05, 320.10, 16)
        str3 = f'\tfloat[16] numbers with range(290.05, 320.10):"""\n\n'
        calculating(in3, file, 3, str3)
        in4 = np.random.uniform(290.05, 320.10, 16)
        str4 = f'\tfloat[16] numbers with range(290.05, 320.10):"""\n\n'
        calculating(in4, file, 4, str4)
        in5 = np.random.uniform(290.05, 320.10, 16)
        str5 = f'\tfloat[16] numbers with range(290.05, 320.10):"""\n\n'
        calculating(in5, file, 5, str5)
        in6 = np.random.uniform(290.05, 320.10, 16)
        str6 = f'\tfloat[16] numbers with range(290.05, 320.10):"""\n\n'
        calculating(in6, file, 6, str6)
        in7 = np.random.uniform(290.05, 320.10, 16)
        str7 = f'\tfloat[16] numbers with range(290.05, 320.10):"""\n\n'
        calculating(in7, file, 7, str7)
        in8 = np.random.uniform(290.05, 320.10, 16)
        str8 = f'\tfloat[16] numbers with range(290.05, 320.10):"""\n\n'
        calculating(in8, file, 8, str8)
        in9 = np.random.uniform(290.05, 320.10, 16)
        str9 = f'\tfloat[16] numbers with range(290.05, 320.10):"""\n\n'
        calculating(in9, file, 9, str9)

        file.close()
    except FileExistsError as e:
        print(f'Error: {e}')

main()