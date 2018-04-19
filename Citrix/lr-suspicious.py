import csv
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import os
import nltk
import numpy as np


#将选择的component类型作为正例，其位置置1，其他类别则置0，返回一维数组
def SelectType(component_type,typename):
    types = []
    for x in component_type:
        if x == typename:
            types.append(1)
        else:
            types.append(0)
    return types

def ReadCSVFile(filepath,encoding='utf-8'):
    data = []
    with open(filepath,'r',encoding=encoding,) as f:
        reader = csv.reader(f)
        for i in reader:
            data.append(i)
    print('has read {length} data.'.format(length=len(data)))
    return data

#获取指定列名的全部信息；
#所有的列名'Id', 'CaseNumber', 'Service Product Consolidated', 'ProblemType', 'Date Created', 'Age/TTC', 'Severity', 'Product Component', 'Status', 'Product Version', 'Subject', 'Description', 'Resolution', 'Cause'
def GetOneColumnData(source,column_name):
    column_list = source[0]
    column_data = []
    if column_name not in column_list:
        print('{column_name} not exists!'.format(column_name=column_name))
    else:
        column_index = source[0].index(column_name)
        for i in source[1:]:
            column_data.append(i[column_index])
    print('get {column_length} {column_name} data!'.format(column_length=len(column_data),column_name=column_name))
    return column_data

def WriteToCsv(csv_path,*args):
    #如果没这个文件，第一行先生成列名
    if not os.path.exists(csv_path):
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            first_column = ['component_type', 'description', 'resolution','index_13w']
            writer = csv.writer(f)
            writer.writerow(first_column)
    #写入训练后的测试数据
    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([args[0],args[1],args[2],args[3]])
        print('successfully writing!')
    return

#获取所有component的类别
def GetALLDiffKindOfComponents(component_list):
    kinds = []
    for i in component_list:
        if i not in kinds:
            kinds.append(i)
    return kinds

#计算这个种类的component的数量
def CalThisKindComponentAccount(one_component_type_list):
    quantity = 0
    for i in one_component_type_list:
        if i == 1:
            quantity += 1
    return quantity



#读取文件
csv_data = ReadCSVFile('../../info/cleandata_13w_PSDR.csv')
product_component = GetOneColumnData(csv_data,'Product Component')
description = GetOneColumnData(csv_data,'Description')
resolution = GetOneColumnData(csv_data,'Resolution')
kinds = GetALLDiffKindOfComponents(product_component)

#type指product_component的一个种类
type = 'Database'
component_type_list = SelectType(product_component,type)
type_quantity = CalThisKindComponentAccount(component_type_list)

#添加resolution
data = []
for p,q in zip(description,resolution):
    data.append(p+' '+q)

# 计算文本TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(data)  # 计算每个词语的tf-idf权值

#自己实现分组
y = component_type_list
l1=int(0.7*len(y))
print(l1)
X_train=X[:l1]
X_test=X[l1:]
y_train=y[:l1]
y_test=y[l1:]

# 使用LR模型训练
lgs = LogisticRegression(penalty='l2', class_weight='balanced',C=1)
lgs.fit(X_train, y_train)



#找出可能错分的文本
suspicious = []
p = lgs.predict_proba(X_test)#分类概率

for i in range(len(p)):
    description_index = 91857 + i
    if p[i][0]>0.95 and y_test[i]==1:
        suspicious.append([description[description_index],resolution[description_index],description_index+2])#+2是为了和csv文档中的行数一致

for i in suspicious:
    print(i)
print(len(suspicious))
path = '../../info/result/suspicious-DR.csv'
for x in suspicious:
    WriteToCsv(path,type,x[0],x[1],x[2])