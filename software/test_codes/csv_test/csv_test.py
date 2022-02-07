import csv

with open('cows.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        print(row)