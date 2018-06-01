import csv
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import os
import pickle
from sklearn.externals import joblib
import nltk
from sklearn.decomposition import TruncatedSVD
import numpy as np

def ReadCSVFile(filepath,encoding='utf-8'):
    data = []
    with open(filepath,'r',encoding=encoding,) as f:
        reader = csv.reader(f)
        for i in reader:
            data.append(i)
    print('read {length} data from csv file.'.format(length=len(data)))
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

def WriteTrainDataToCsv(csv_path,data):
    #写入训练后的测试数据
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for i in data:
            writer.writerow(i)
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
def CalThisKindComponentAccount(component_list,component_name):
    quantity = 0
    for i in component_list:
        if i == component_name:
            quantity += 1
    return quantity

#获取列表中数值最大的前n个数的下标，返回的是下标的数组
def GetTopNProba(l,n):
    top = []
    ll = l.copy()
    for i in range(n):
        top.append(ll.index(max(ll)))
        ll[top[-1]] = 0
    return top

def GetALLDiffKindOfComponents(component_list):
    kinds = []
    for i in component_list:
        if i not in kinds:
            kinds.append(i)
    return kinds

def GetMoreThanXXXPieceOfComponentData(data,XXX):
    component_row_index = csv_data[0].index('Product Component')
    less_than_200 = []
    kind_quantity = {}
    product_component = GetOneColumnData(data, 'Product Component')
    kinds = GetALLDiffKindOfComponents(product_component)
    print('less than {num} component will be filter!'.format(num = XXX))
    print('before filter, there are {num} kinds of components,total {piece} data!'.format(num=len(kinds),piece=len(data)))
    for i in kinds:
        kind_quantity[i] = 0
    for i in data[1:]:
        for j in kinds:
            if i[component_row_index] == j:
                kind_quantity[j] += 1
    for key, value in kind_quantity.items():
            if value < 200:
                less_than_200.append(key)
    # print(less_than_200)
    for i in data[:0:-1]:
        if i[component_row_index] in less_than_200:
            data.remove(i)
    print('after filter, there are {num} kinds of components,total {piece} data!'.format(num=(len(kinds) - len(less_than_200)), piece=len(data)))
    return data

def GetTopNComponentNames(csv_data,n):
    n_component_name = []
    component_quantity = []
    component_list = GetOneColumnData(csv_data,'Product Component')
    all_component_name = GetALLDiffKindOfComponents(component_list)
    for name in all_component_name:
        component_quantity.append([name,CalThisKindComponentAccount(component_list,name)])
    component_quantity_sort = sorted(component_quantity, key=lambda x: x[1], reverse=True)
    for i in range(n):
        n_component_name.append(component_quantity_sort[i][0])
    return n_component_name

def GetTopNComponentData(csv_data,n):
    component_row_index = csv_data[0].index('Product Component')
    data = []
    data.append(csv_data[0])
    component_name = GetTopNComponentNames(csv_data,n)
    for i in csv_data[1:]:
        if i[component_row_index] in component_name:
            data.append(i)
    print('total {component_kinds_len} components with {data_len} piece of data'.format(component_kinds_len=len(component_name),data_len=len(data)))
    return data

def SelectColumnData(description,resolution,cause,subject,n):
    column = [description,resolution,cause,subject]
    data = []
    for i in range(len(description)):
        s = ''
        for j in range(n):
            s +=(column[j][i]+' ')
        data.append(s)
    return data
def GetTopNClassifyNameAndProba(predict_proba,classes,n):
    p = predict_proba.tolist()
    classnames = []
    for k in range(len(p)):
        name_index = GetTopNProba(p[k], n)
        name = []
        for i in name_index:
            name.append(classes[i])
            name.append(round(p[k][i],3))
        classnames.append(name)
    return classnames
#读取文件
#csv_data = ReadCSVFile('../../info/cleandata_13w_PSDRC.csv')
#csv_data = ReadCSVFile('../../info/cleandata_12w_PSDR.csv')
#csv_data = ReadCSVFile('../../info/cleandata_10w_ctx.csv')
#csv_data = ReadCSVFile('../../info/cleandata_9w_nohttp.csv')
csv_data = ReadCSVFile('../../info/newcleandata.csv')

#csv_data = GetMoreThanXXXPieceOfComponentData(csv_data,,45)#把总量比较少的component数据去掉
csv_data = GetTopNComponentData(csv_data,60)#只取数量前n的component数据
case_id = GetOneColumnData(csv_data,'Id')
case_number = GetOneColumnData(csv_data,'CaseNumber')
product_component = GetOneColumnData(csv_data,'Product Component')
subject = GetOneColumnData(csv_data,'Subject')
description = GetOneColumnData(csv_data,'Description')
resolution = GetOneColumnData(csv_data,'Resolution')
cause = GetOneColumnData(csv_data,'Cause')

#选择使用哪几个column作为训练数据，n代表选前n个
newdata = SelectColumnData(description,resolution,cause,subject,2)

#控制训练集比例
percentage = int(0.8*len(newdata))

# 计算文本TF-IDF
vectorizer = TfidfVectorizer(stop_words='english',sublinear_tf=True,ngram_range=(1,2))
X = vectorizer.fit_transform(newdata)  # 计算每个词语的tf-idf权值
X_train = X[:percentage]

# 切割训练集和测试集
y = product_component
y_train = y[:percentage]

#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)


# 使用LR模型训练
lgs = LogisticRegression(penalty='l2', class_weight='balanced',C=5)

#使用随机森林模型
#lgs = RandomForestClassifier(n_estimators=100)
lgs.fit(X_train, y_train)


X_test = X[percentage:]
y_test = y[percentage:]

#自己写分类策略
p = lgs.predict(X_test)
accuracy = metrics.accuracy_score(y_test, p)
print(accuracy)
pp = lgs.predict_proba(X_test)
def GetTopNClassifyName(predict_proba,classes,n):
    p = predict_proba.tolist()
    classnames = []
    for k in range(len(p)):
        name_index = GetTopNProba(p[k], n)
        name = []
        for i in name_index:
            name.append(classes[i])
        classnames.append(name)
    return classnames

c=GetTopNClassifyName(pp,lgs.classes_,3)

# not top3
cc = GetTopNClassifyNameAndProba(pp,lgs.classes_,3)
mydata = []
n=0
data = csv_data[percentage+1:]
print(len(data))
print(len(y_test))
index = 0
for i,j in zip(y_test,c):
    if i in j:
        n+=1
    else:
        dd=data[index]+cc[index]
        mydata.append(dd)
    index+=1
print(n/len(y_test))

# mydata = []
# print(len(csv_data[percentage+1:]))
# print(len(p))
# for i in range(len(p)):
#     onedata = csv_data[1 + percentage + i]
#     if onedata[0] == p[i] and max(pp[i])>0.9:
#         onedata.append(max(pp[i]))
#         onedata.append(p[i])
#         onedata.append('TP')
#         mydata.append(onedata)
#     else:
#         if onedata != p[i] and max(pp[i])>0.9:
#             onedata.append(max(pp[i]))
#             onedata.append(p[i])
#             onedata.append('TN')
#             mydata.append(onedata)

# csv_path = '../../info/11111111111111111.csv'
# WriteTrainDataToCsv(csv_path,mydata)