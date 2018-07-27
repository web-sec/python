#coding:utf-8
import nltk
import csv
import os
import string
import datetime
import re
import xlrd

def ReadCSVFile(filepath,encoding='utf-8'):
    data = []
    with open(filepath,'r',encoding=encoding) as f:
        reader = csv.reader((line.replace('\0', '') for line in f))
        for i in reader:
            data.append(i)
    return data


def GetTranslateData(path='../../../info/SmartTool/alldata/salesforce_vs_sc_account_mapping.xlsx'):
    data = xlrd.open_workbook(path)
    table = data.sheets()[0]
    nrows = table.nrows #行数
    data={}
    for i in range(nrows):
        rowValues= table.row_values(i) #某一行数据
        if len(rowValues)==2:
            data[rowValues[0]]=rowValues[1]
    return data

def GetIssueData(path='../../../info/SmartTool/alldata/issues_list_new.csv'):
    data = ReadCSVFile(path)
    newdata = []
    for i in data[1:]:
        newdata.append([i[1],i[-2],i[-1]])#[isseu_key,issue_description,issue_resolution]
    return newdata

translate_data = GetTranslateData()
issue_data = GetIssueData()
rule = re.compile(r'\d+')
err_data = ReadCSVFile('newdata.csv')
case_data = ReadCSVFile('../../../info/SmartTool/alldata/48w_ts_cases_from_20160101.csv')
data = ReadCSVFile('mydata.csv')
newdata = []
n=0
for i in data[1:]:
    n+=1
    print(n)
    for j in issue_data:
        if i[1] == j[0]:
            i.insert(2,j[1])
            i.insert(3,j[2])
    for k in case_data:
        if i[8] == k[0]:
            i.insert(9,k[-4])
            i.insert(10, k[-3])
    newdata.append(i)
with open('mydata2.csv','w',newline='',encoding='utf-8') as f:
    writer = csv.writer(f)
    # writer.writerow(['Product Component','Subject','Description','Resolution'])
    for x in newdata:
        writer.writerow(x)