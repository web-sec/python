import csv
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import os
import nltk
from sklearn.decomposition import TruncatedSVD
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

def WriteTrainDataToCsv(csv_path,algorithm,data_quantity, component_type, accuracy, precision, recall, f1, auc):
    #如果没这个文件，第一行先生成列名
    if not os.path.exists(csv_path):
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            first_column = ['algorithm','data_quantity', 'component_type', 'accuracy', 'precision', 'recall', 'f1', 'auc']
            writer = csv.writer(f)
            writer.writerow(first_column)
    #写入训练后的测试数据
    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([algorithm,data_quantity,component_type, accuracy, precision, recall, f1, auc])
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
kinds = GetALLDiffKindOfComponents(product_component)
#type指product_component的一个种类
typename = 'Controller'
component_type_list = SelectType(product_component,typename)
type_quantity = CalThisKindComponentAccount(component_type_list)

X = ReadCSVFile('DR_model_300.csv')
for i in range(len(X)):
    for j in range(len(X[i])):
        X[i][j] = float(X[i][j])

print('{type} 类型共有 {num} 条！'.format(type=typename,num=type_quantity))
y = component_type_list
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)


# 使用LR模型训练
lgs = LogisticRegression(penalty='l2', class_weight='balanced',C=1)
lgs.fit(X_train, y_train)

predicted = lgs.predict(X_test)

# 用各种度量标准基于测试集结果评价模型
# predicted = lgs.predict(X_test)
accuracy = metrics.accuracy_score(y_test, predicted)
precision = metrics.precision_score(y_test, predicted)
recall = metrics.recall_score(y_test, predicted)
f1 = metrics.f1_score(y_test, predicted)
auc = metrics.roc_auc_score(y_test, predicted)

print('types:' + typename)
print('accuracy: {accuracy}'.format(accuracy=accuracy))
print('precision: {precision}'.format(precision=precision))
print('recall: {recall}'.format(recall=recall))
print('f1: {f1}'.format(f1=f1))
print('auc: {auc}'.format(auc=auc))