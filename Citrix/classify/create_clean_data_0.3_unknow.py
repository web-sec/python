#coding:utf-8
import nltk
from nltk.stem.porter import *
import csv
import string
from nltk.corpus import stopwords
from collections import Counter

def ReadCSVFile(filepath,encoding='utf-8'):
    data = []
    with open(filepath,'r',encoding=encoding) as f:
        reader = csv.reader(f)
        data.append(next(reader))
        for i in reader:
            if i[7] == 'No Applicable Component' or i[7] == 'Unspecified':
                if not IsNotEnglishData(i):
                    data.append(i)
    print('has read {length} data.'.format(length=len(data)))
    return data

#获取指定列名的全部信息；
def GetOneColumnData(source,column_name):
    column_list = source[0]
    column_data = []
    if column_name not in column_list:
        print('{column_name} not exists!'.format(column_name=column_name))
    else:
        column_index = source[0].index(column_name)
        for i in source[1:]:
            try:
                column_data.append(i[column_index])
            except:
                column_data.append('N/A')
    print('get {column_length} {column_name} data!'.format(column_length=len(column_data),column_name=column_name))
    return column_data

def NotEnglish(string):
    for c in string:
        if ord(c) > 128:
            return True
    return False

def IsNotEnglishData(one_piece_of_data):
    if len(one_piece_of_data)<13:
        return True
    else:
        for i in [10,11,12]:
            if NotEnglish(one_piece_of_data[i]):
                return True
        return False


csv_data = ReadCSVFile('../../info/all.csv')#读取文件
component = GetOneColumnData(csv_data,'Product Component')
description = GetOneColumnData(csv_data,'Description')
subject = GetOneColumnData(csv_data,'Subject')
resolution = GetOneColumnData(csv_data,'Resolution')
cause = GetOneColumnData(csv_data,'Cause')
print(len(csv_data))


with open('../../info/newcleandata.csv','w',newline='',encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Product Component','Subject','Description','Resolution','Cause'])
    for x,y,z,p,q in zip(component,subject,description,resolution,cause):
        writer.writerow([x,y,z,p,q])