#coding:utf-8
import nltk
import csv

def ReadCSVFile(filepath,encoding='utf-8'):
    data = []
    with open(filepath,'r',encoding=encoding) as f:
        reader = csv.reader(f)
        data.append(next(reader))
        for i in reader:
            if not IsIllegalData(i):
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


def IsIllegalData(one_piece_of_data):
    illegal_data = ['No Applicable Component','Unspecified','Desktop VDA','Server VDA' ,'n/a' ,'N/A','NULL']
    for i in [9,16]:
        if one_piece_of_data[i] in illegal_data or NotEnglish(one_piece_of_data[i]):
            return True
    return False

csv_data = ReadCSVFile('../../info/onefix.csv')#读取文件
title= GetOneColumnData(csv_data,'Title')
problem_description= GetOneColumnData(csv_data,'ProblemDescription')
rootCause= GetOneColumnData(csv_data,'RootCause')
resolution_text= GetOneColumnData(csv_data,'ResolutionText')
case_number= GetOneColumnData(csv_data,'CaseNumber')
component = GetOneColumnData(csv_data,'Component')
description = GetOneColumnData(csv_data,'Description')
all_data = []
for i in range(len(title)):
    all_data.append([title[i],problem_description[i],rootCause[i],resolution_text[i],case_number[i],component[i],description[i]])
with open('../../info/newcleandata.csv','w',newline='',encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Title','ProblemDescription','RootCause','ResolutionText','CaseNumber','Component','Description'])
    for i in all_data:
        writer.writerow(i)