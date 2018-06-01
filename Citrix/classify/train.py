import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import os
import nltk
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle
from sklearn.externals import joblib

def ReadCSVFile(filepath,encoding='utf-8'):
    data = []
    with open(filepath,'r',encoding=encoding,) as f:
        reader = csv.reader(f)
        for i in reader:
            data.append(i)
    print('has read {length} data.'.format(length=len(data)))
    return data
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
def GetALLDiffKindOfComponents(component_list):
    kinds = []
    for i in component_list:
        if i not in kinds:
            kinds.append(i)
    return kinds
def CalThisKindComponentAccount(component_list,component_name):
    quantity = 0
    for i in component_list:
        if i == component_name:
            quantity += 1
    return quantity
def GetTopNProba(probability_list,n_length):
    top = []
    p = probability_list
    for i in range(n_length):
        top.append(p.index(max(p)))
        p[top[-1]] = 0
    return top
def GetTopNClassifyName(predict_proba,classes,n):
    classnames = []
    if type(predict_proba) == type(np.array([1])):
        p = predict_proba.tolist()
        for k in range(len(p)):
            name_index = GetTopNProba(p[k], n)
            name = []
            for i in name_index:
                name.append(classes[i])
            classnames.append(name)
    elif type(predict_proba) == type([1]):
        p = predict_proba
        name_index = GetTopNProba(p, n)
        for i in name_index:
            classnames.append(classes[i])
    return classnames
csv_data = ReadCSVFile('../../info/cleandata_11w_PSDR_45component.csv')
product_component = GetOneColumnData(csv_data,'Product Component')
description = GetOneColumnData(csv_data,'Description')
resolution = GetOneColumnData(csv_data,'Resolution')
data = []
for p,q in zip(description,resolution):
    data.append(p+' '+q)
vectorizer = TfidfVectorizer(stop_words='english',sublinear_tf=True)

# data = description

X = vectorizer.fit_transform(data)
#导出tfidf模型
# output = open('tfidf_DR_45component.pkl', 'wb')
# pickle.dump(vectorizer,output)

#导入tfidf模型
# output = open('tfidf_DR.pkl', 'rb')
# vectorizer = pickle.load(output)


y = product_component
# lgs = LogisticRegression(penalty='l2', class_weight='balanced',C=3)
lgs = RandomForestClassifier(n_estimators=120)
lgs.fit(X,y)

joblib.dump(lgs,'RF_DR.pkl')
