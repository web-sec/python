import numpy as np
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
def DeleteNan(s1,s2):
    nan = float('nan')
    amount = 0
    for i in range(len(s1)-1,-1,-1):
        if type(s2[i]) == type(nan):
            amount += 1
            del (s2[i])
            del (s1[i])
    print('delete {amount} nan text'.format(amount=amount))

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
csv_data = ReadCSVFile('../../info/cleandata_12w_PSDR.csv')
product_component = GetOneColumnData(csv_data,'Product Component')
description = GetOneColumnData(csv_data,'Description')
resolution = GetOneColumnData(csv_data,'Resolution')

# 计算文本TF-IDF
vectorizer = TfidfVectorizer(stop_words='english',sublinear_tf=True)
X = vectorizer.fit_transform(description)  # 计算每个词语的tf-idf权值
X_train = X[:100000]

# 切割训练集和测试集
y = product_component
y_train = y[:100000]

#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)


# 使用LR模型训练
rf = RandomForestClassifier(n_estimators=100)
rf.fit(X_train, y_train)
X_test = X[100000:]
y_test = y[100000:]
#自己写分类策略
#p = lgs.predict_proba(X_test)#分类概率
p = rf.predict(X_test)
accuracy = metrics.accuracy_score(y_test, p)
print(accuracy)
pp = rf.predict_proba(X_test)
def GetTopNProba(l,n):
    top = []
    for i in range(n):
        top.append(l.index(max(l)))
        l[top[-1]] = 0
    return top
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

c=GetTopNClassifyName(pp,rf.classes_,3)
n=0
for i,j in zip(y_test,c):
    if i in j:
        n+=1
print(n/len(y_test))
