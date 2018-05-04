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
import re

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

def WriteToCsv(csv_path,data):
    #如果没这个文件，第一行先生成列名
    if not os.path.exists(csv_path):
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            first_column = ['0-1','initial_component_type','classification_results', 'description', 'resolution','posibility','index_13w']
            writer = csv.writer(f)
            writer.writerow(first_column)
    #写入训练后的测试数据
    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(data)
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


def GetTop10(l):
    if len(l)<=10:
        return l
    else:
        l.sort(key = lambda a:a[5])
        return l[:10]
#读取文件
csv_data = ReadCSVFile('../../info/cleandata_13w_PSDR.csv')
product_component = GetOneColumnData(csv_data,'Product Component')
description = GetOneColumnData(csv_data,'Description')
resolution = GetOneColumnData(csv_data,'Resolution')
kinds = GetALLDiffKindOfComponents(product_component)
newdata = []
for p,q in zip(description,resolution):
    newdata.append(p+' '+q)

# 计算文本TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(newdata)  # 计算每个词语的tf-idf权值

#文本映射
patterns = [re.compile(r'client drive'),re.compile(r'client drives'),re.compile(r'client drive mapping'),re.compile(r'client drives mapping'),re.compile(r'client mapping'),re.compile(r'client mapping drive'),re.compile(r'client mapping drives'),re.compile(r'drive mapping'),re.compile(r'CMD')]
for i in range(len(newdata)):
    for j in patterns:
        newdata[i] = re.sub(j,'CDM',newdata[i])

#typename指product_component的一个种类
for typename in kinds:
    component_type_list = SelectType(product_component,typename)
    type_quantity = CalThisKindComponentAccount(component_type_list)
    if type_quantity < 200:
        continue

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
    suspicious1 = []
    suspicious2 = []
    suspicious3 = []
    p = lgs.predict_proba(X_test)#分类概率
    #模型认为正例，实际负例
    for i in range(len(p)):
        description_index = 91857 + i
        if p[i][1]>0.90 and y_test[i]==0:
            suspicious1.append(['FP',product_component[description_index],typename,description[description_index],
                                resolution[description_index],p[i][1],description_index+2])#+2是为了和csv文档中的行数一致

    #模型认为负例，实际正例
    for i in range(len(p)):
        description_index = 91857 + i
        if p[i][0] > 0.90 and y_test[i] == 1:
            suspicious1.append(['FN',product_component[description_index], 'non-'+typename, description[description_index],
                                resolution[description_index], p[i][0], description_index + 2])

    #模型认为正例，实际正例
    for i in range(len(p)):
        description_index = 91857 + i
        if p[i][1] > 0.90 and y_test[i] == 1:
            suspicious1.append(['TP',product_component[description_index], typename, description[description_index],
                                resolution[description_index], p[i][1], description_index + 2])

    suspicious = GetTop10(suspicious1) + GetTop10(suspicious2) + GetTop10(suspicious3)
    path = 'show.csv'
    for x in suspicious:
        WriteToCsv(path,x)