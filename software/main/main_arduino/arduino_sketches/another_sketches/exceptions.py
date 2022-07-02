#exceptions
# try: 
#     1/0
# except ZeroDivisionError:
#     k = 0
# print(k)

f = open('1.txt')
ints = []
try:
    for line in f:
        ints.append(int(line))
    print(ints)
except ValueError:
    print('It is not a number. Exit')
except Exception:
    print('What is that?')
else:
    print('All right!')
finally:
    f.close()
    print('I close the file.')

