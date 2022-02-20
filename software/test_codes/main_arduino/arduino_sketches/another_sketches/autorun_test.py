from datetime import datetime
import csv

i = 0

while i < 100:
    date_now = str(datetime.now())
    row = [i, date_now, 999]
    with open('time.csv', 'a', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(row)
    writeFile.close()
    i += 1from datetime import datetime
import csv

i = 0

while i < 100:
    date_now = str(datetime.now())
    row = [i, date_now, 999]
    with open('time.csv', 'a', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(row)
    writeFile.close()
    i += 1