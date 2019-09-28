import csv
row = ['5', ' Danny', ' New York']
with open('people.csv', 'a') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(row)
csvFile.close()