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
    for i in range(n):
        top.append(l.index(max(l)))
        l[top[-1]] = 0
    return top

def GetALLDiffKindOfComponents(component_list):
    kinds = []
    for i in component_list:
        if i not in kinds:
            kinds.append(i)
    return kinds

def GetMoreThanXXXPieceOfComponentData(data,XXX):
    less_than_200 = []
    kind_quantity = {}
    product_component = GetOneColumnData(data, 'Product Component')
    kinds = GetALLDiffKindOfComponents(product_component)
    print('less than {num} will be filter!'.format(num = XXX))
    print('before filter, there are {num} kinds of components,total {piece} data!'.format(num=len(kinds),piece=len(data)))
    for i in kinds:
        kind_quantity[i] = 0
    for i in data[1:]:
        for j in kinds:
            if i[0] == j:
                kind_quantity[j] += 1
    for key, value in kind_quantity.items():
            if value < 200:
                less_than_200.append(key)
    # print(less_than_200)
    for i in data[:0:-1]:
        if i[0] in less_than_200:
            data.remove(i)
    print('after filter, there are {num} kinds of components,total {piece} data!'.format(num=(len(kinds) - len(less_than_200)), piece=len(data)))
    return data

#读取文件
#csv_data = ReadCSVFile('../../info/cleandata_9w_nohttp.csv')
csv_data = ReadCSVFile('../../info/cleandata_12w_PSDR.csv')

csv_data = GetMoreThanXXXPieceOfComponentData(csv_data,200)#把总量比较少的component数据去掉

product_component = GetOneColumnData(csv_data,'Product Component')
description = GetOneColumnData(csv_data,'Description')
resolution = GetOneColumnData(csv_data,'Resolution')

#使用description和resolution同时作为训练数据
newdata = []
for p,q in zip(description,resolution):
    newdata.append(p+' '+q)
newdata=resolution

#控制训练集比例
percentage = int(0.7*len(newdata))

# 计算文本TF-IDF
vectorizer = TfidfVectorizer(stop_words='english',sublinear_tf=True)
X = vectorizer.fit_transform(newdata)  # 计算每个词语的tf-idf权值
X_train = X[:percentage]

# 切割训练集和测试集
y = product_component
y_train = y[:percentage]

#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)


# 使用LR模型训练
# lgs = LogisticRegression(penalty='l2', class_weight='balanced',C=1)

#使用随机森林模型
lgs = RandomForestClassifier(n_estimators=120)
lgs.fit(X_train, y_train)


X_test = X[percentage:]
y_test = y[percentage:]

#自己写分类策略
#p = lgs.predict_proba(X_test)#分类概率
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
n=0
for i,j in zip(y_test,c):
    if i in j:
        n+=1
print(n/len(y_test))
#csv_path = '../../info/N_V_num_filter_13w.csv'
#WriteTrainDataToCsv(csv_path,'LR', '{len_types}/{len_all}'.format(len_types=type_quantity, len_all=len(product_component)),type, accuracy, precision, recall, f1, auc)

# p = lgs.predict(X_test)
# data = []
# for i in range(len(p)):
#     data.append([y_test[i],p[i],description[100000+i],resolution[100000+i]])
#
# csv_path = '../../info/123_13w.csv'
# WriteTrainDataToCsv(csv_path,data)