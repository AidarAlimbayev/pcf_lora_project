import csv
row = ['2', ' john', ' California']

with open('people.csv', 'r') as readFile:
    reader = csv.reader(readFile)
    lines = list(reader)
    lines[2] = row

with open('people.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(lines)
    
readFile.close()
writeFile.close()