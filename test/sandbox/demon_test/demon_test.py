import datetime
current_time = datetime.datetime.now()
name = '/home/pi/Desktop/MyStartUp/' + str(current_time) + '.txt'
f= open(name,"w+")
f.write("Текущее время загрузки Raspberry Pi " + str(current_time) + '\r\n')
for i in range(10):
     f.write("Это строка номер %d\r\n" % (i+1))
f.close()