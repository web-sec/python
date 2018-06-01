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
            data.append(i)
    print('has read {length} data.'.format(length=len(data)))
    return data

def IsSameNumbers(number_list):
    flag = 0
    l = len(number_list)
    for i in range(l):
        for j in range(i,l):
            if number_list[i] != number_list[j]:
                flag+=1
    if flag > 0:
        return False
    else:
        return True

def GetCTXNumber(s):
    rule = re.compile(r'http[s]?://support\S*CTX(\d+)')
    number_list = rule.findall(s)
    if len(number_list)>0:
        if IsSameNumbers(number_list):
            return number_list[0]

def GetAllKBNumber(filepath,casenumber_column_index=1,description_column_index=12):
    csv_data = ReadCSVFile(filepath)#读取文件
    data = []
    for i in csv_data:
        if len(i) > description_column_index:
            number = GetCTXNumber(i[description_column_index])
            if number != None:
                data.append([i[casenumber_column_index],number])
    return data

def WriteToCSV(data,filepath='newdata.csv'):
    with open(filepath,'w',newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        for i in data:
            writer.writerow(i)

if __name__ == '__main__':
    data = GetAllKBNumber('../../info/all.csv')
    WriteToCSV(data)