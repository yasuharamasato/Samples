import csv
import datetime
import os

path=os.path.dirname(os.path.abspath(__file__))

with open(path+'/test.csv', 'w') as csv_file:
    fieldnames = ['time', 'io']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    
    dt=datetime.datetime.now()
    num=10
    for i in range(num):
        writer.writerow({'time': dt, 'io': i})
        dt = dt + datetime.timedelta(minutes=10*i)

with open(path+'/test2.csv', 'w') as csv_file:
    fieldnames = ['time', 'io']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    
    dt=datetime.datetime.now()
    num=7
    for i in range(num):
        writer.writerow({'time': dt, 'io': i-1})
        dt = dt + datetime.timedelta(minutes=10*i)