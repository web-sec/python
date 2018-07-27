# coding:utf-8
import nltk
import csv
import os
import string
import datetime
import re
import xlrd


def ReadCSVFile(filepath, encoding='utf-8'):
    data = []
    with open(filepath, 'r', encoding=encoding) as f:
        reader = csv.reader((line.replace('\0', '') for line in f))
        for i in reader:
            data.append(i)
    return data


rule = re.compile(r'CTX(\d+)')
data = ReadCSVFile('mydata2.csv')
newdata = []
n = 0
for i in data:
    ctx_issue = list(set(rule.findall(i[3])))
    ctx_case = list(set(rule.findall(i[10])))
    if len(ctx_case) == 1 and len(ctx_issue) == 1:
        if ctx_issue[0] == ctx_case[0]:
            i.append('YES')
    if len(ctx_case) > 1:
        if len([val for val in ctx_case if val in ctx_issue]) > 0:
            i.append('Maybe')
    if len(i) == 13:
        i.append('NO')
    newdata.append(i)

# with open('mydata3.csv', 'w', newline='', encoding='utf-8') as f:
#     writer = csv.writer(f)
#     # writer.writerow(['Product Component','Subject','Description','Resolution'])
#     for x in data:
#         writer.writerow(x)
