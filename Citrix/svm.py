import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn import svm
import os

def DeleteNan(s1,s2):#删除s2列表中的NAN，同时删除对应下标的s1中的信息
    nan = float('nan')
    amount = 0
    for i in range(len(s1)-1,-1,-1):
        if type(s2[i]) == type(nan):
            amount += 1
            del (s2[i])
            del (s1[i])
    print('delete {amount} nan text'.format(amount=amount))

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

def GetALLDiffKindOfComponents(component_list):
    kinds = []
    for i in component_list:
        if i not in kinds:
            kinds.append(i)
    return kinds
def CalThisKindComponentAccount(one_component_type_list):
    quantity = 0
    for i in one_component_type_list:
        if i == 1:
            quantity += 1
    return quantity

csv_data = ReadCSVFile('../../info/cleandata_13w_PSDR.csv')#读取文件
product_component = GetOneColumnData(csv_data,'Product Component')
description = GetOneColumnData(csv_data,'Description')
DeleteNan(product_component,description)
kinds = GetALLDiffKindOfComponents(product_component)

type = 'Controller'
component_type_list = SelectType(product_component,type)
type_quantity = CalThisKindComponentAccount(component_type_list)

print('{type} 类型共有 {num} 条！'.format(type=type,num=type_quantity))

#计算文本TF-IDF
vectorizer = TfidfVectorizer(stop_words = 'english')
X = vectorizer.fit_transform(description)#计算每个词语的tf-idf权值

#切割训练集和测试集
y = component_type_list
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

#使用SVM模型训练
clf = svm.SVC(C=1, kernel='linear')
clf.fit(X_train, y_train)

#将模型运用在测试集上
predicted = clf.predict(X_test)

#用各种度量标准基于测试集结果评价模型
accuracy = metrics.accuracy_score(y_test,predicted)
precision = metrics.precision_score(y_test,predicted)
recall = metrics.recall_score(y_test,predicted)
f1 = metrics.f1_score(y_test,predicted)
auc = metrics.roc_auc_score(y_test,predicted)

print('types:'+type)
print('accuracy: {accuracy}'.format(accuracy=accuracy))
print('precision: {precision}'.format(precision=precision))
print('recall: {recall}'.format(recall=recall))
print('f1: {f1}'.format(f1=f1))
print('auc: {auc}'.format(auc=auc))



