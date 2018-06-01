#coding:utf-8
import csv
def ReadCSVFile(filepath,encoding='utf-8'):
    data = []
    with open(filepath,'r',encoding=encoding) as f:
        reader = csv.reader(f)
        for i in reader:
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


def DeleteIllegalData(component,description,subject,resolution):
    for i in range(len(component) - 1, -1, -1):
        #将不要的component类别名写入判断中
        if component[i] == 'No Applicable Component' or component[i] == 'Unspecified' or component[i] == 'Desktop VDA' or component[i] == 'Server VDA' or description[i] == 'n/a' or description[i] == 'N/A':
            del (component[i])
            del (description[i])
            del (subject[i])
            del (resolution[i])
        else:#非英文字符
            for c in description[i]:
                if ord(c) > 128:
                    del (component[i])
                    del (description[i])
                    del (subject[i])
                    del (resolution[i])
                    break

    return
csv_data = ReadCSVFile('../../info/all.csv')#读取文件
component = GetOneColumnData(csv_data,'Product Component')
description = GetOneColumnData(csv_data,'Description')
subject = GetOneColumnData(csv_data,'Subject')
resolution = GetOneColumnData(csv_data,'Resolution')
print(len(component),len(description),len(subject),len(resolution))

DeleteIllegalData(component,description,subject,resolution)
print(len(component),len(description),len(subject),len(resolution))
#
# with open('../../info/newcleandata.csv','w',newline='',encoding='utf-8') as f:
#     writer = csv.writer(f)
#     writer.writerow(['Product Component','Subject','Description'])
#     for x,y,z in zip(component,subject,description):
#         writer.writerow([x,y,z])