import csv
import os
import pandas as pd
from csv import reader
from datetime import datetime
import datetime as dt

path=os.path.dirname(os.path.abspath(__file__))
#サイクルタイムの信号を処理する
#input:log/Logfile
#output:bunseki/Logfile
def add(file_name):
    df = pd.read_csv(path+'/log/'+file_name, header=0, index_col=0)
    if len(df.index)<2:
        return
    
    tail=df.tail(2)
    with open(path+'/bunseki/CT_'+file_name, 'a') as f:
        writer=csv.writer(f)
        writer.writerow([])

    return

def syoki(file_name):
    list_log=[]
    with open(path+'/log/'+file_name, 'r') as csv_file:
        csv_reader = reader(csv_file)
        # Passing the cav_reader object to list() to get a list of lists
        list_log = list(csv_reader)
    if len(list_log)<2:
        return
    print (list_log)
    with open(path+'/bunseki/CT_'+file_name, 'w') as f:
        fieldnames = ['id', '開始','終了','CT','就業時間判定','休憩時間判定','実績数']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer = csv.writer(f)
        for i in range(len(list_log)-2):
            id=list_log[i+1][0]
            start=datetime.strptime(list_log[i+1][1], '%Y-%m-%d %H:%M:%S.%f')
            end=datetime.strptime(list_log[i+2][1], '%Y-%m-%d %H:%M:%S.%f')
            CT=end-start
            syugyou=syugyou_hantei(start,end)
            kyukei=kyukei_hantei(start,end)
            writer.writerow([id,start,end,CT,syugyou,kyukei,i])
    
    return

def kyukei_hantei(start,end):
    df = pd.read_csv(path+'/ini.csv', header=0, index_col=0)
    kys=[]
    for ky in df.iloc[3:10,:].values.tolist():
        if not(pd.isnull(ky[0])):
            ky1=dt.time( int(ky[0].split(':')[0]),int(ky[0].split(':')[1]))
            ky1=dt.datetime.combine(dt.date.today(), ky1)
            ky2=dt.time( int(ky[1].split(':')[0]),int(ky[1].split(':')[1]))
            ky2=dt.datetime.combine(dt.date.today(), ky2)
            kys.append([ky1,ky2])
    print (kys)

    hantei=0
    for ky in kys:
        if not(ky[0]>start or ky[1]<end):
            hantei=1
    if hantei==1:
        return '休憩'
    else:
        return '休憩外'


def syugyou_hantei(start,end):
    df = pd.read_csv(path+'/ini.csv', header=0, index_col=0)
    x=df.at['就業時間','値1']
    t_start=dt.time( int(x.split(':')[0]),int(x.split(':')[1]))
    t_start=dt.datetime.combine(dt.date.today(), t_start)

    x=df.at['就業時間','値2']
    t_end=dt.time( int(x.split(':')[0]),int(x.split(':')[1]))
    t_end=dt.datetime.combine(dt.date.today(), t_end)

    if t_start<start and t_end>end:
        return '就業'
    else:
        return '時間外'


if __name__ == '__main__':
    add()