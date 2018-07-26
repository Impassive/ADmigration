import csv
with open('test.csv') as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
         print(row['username'])