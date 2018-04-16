#coding:utf-8
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
    l = len(one_piece_of_data)
    if l < 14:
        return True
    else:
        illegal_data = ['No Applicable Component','Unspecified','Desktop VDA','Server VDA' ,'n/a' ,'N/A']
        for i in [7,10,11,12]:
            if one_piece_of_data[i] in illegal_data or NotEnglish(one_piece_of_data[i]):
                return True
    return False

csv_data = ReadCSVFile('../../info/all.csv')#读取文件
component = GetOneColumnData(csv_data,'Product Component')
description = GetOneColumnData(csv_data,'Description')
subject = GetOneColumnData(csv_data,'Subject')
resolution = GetOneColumnData(csv_data,'Resolution')
print(len(component),len(description),len(subject),len(resolution))


with open('../../info/newcleandata.csv','w',newline='',encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Product Component','Subject','Description','Resolution'])
    for x,y,z,p in zip(component,subject,description,resolution):
        writer.writerow([x,y,z,p])