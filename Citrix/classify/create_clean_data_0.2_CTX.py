#coding:utf-8
import nltk
from nltk.stem.porter import *
import csv
import string
from nltk.corpus import stopwords
import re
from collections import Counter
def get_simple_tokens(text):#对文章进行分词
    lowers = text.lower()
    #remove the punctuation using the character deletion step of translate
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)#ord()函数返回对应字符的ASCLL值
    no_punctuation = lowers.translate(remove_punctuation_map)#字符串的translate()方法将原字符串的指定字符替换成别的指定字符
    tokens = nltk.word_tokenize(no_punctuation)#可能需要手动下载某数据包，看报错即可
    return tokens

def stem_tokens(tokens):#对相似的次做归并
    stemmer = PorterStemmer()
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def get_final_tokens(text):
    tokens = get_simple_tokens(text)
    filtered = [w for w in tokens if not w in stopwords.words('english')]#可能需要手动下载
    count =stem_tokens(filtered)
    return count

def ReadCSVFile(filepath,encoding='utf-8'):
    data = []
    with open(filepath,'r',encoding=encoding) as f:
        reader = csv.reader(f)
        data.append(next(reader))
        for i in reader:
            data.append(i)
    print('has read {length} data.'.format(length=len(data)))
    return data

#获取指定列名的全部信息；
def GetOneColumnData(source,column_name):
    column_list = source[0]
    column_data = []
    if column_name not in column_list:
        print('{column_name} not exists!'.format(column_name=column_name))
    else:
        column_index = source[0].index(column_name)
        for i in source[1:]:
            try:
                column_data.append(i[column_index])
            except:
                column_data.append('N/A')
    print('get {column_length} {column_name} data!'.format(column_length=len(column_data),column_name=column_name))
    return column_data


def ReplaceCTXNumber(texts):
    rule = re.compile(r'http[s]?://support.citrix.com/article/')
    for i in range(len(texts)):
        texts[i] = re.sub(rule, '', texts[i])

def GetBadIndexInResolution(s):
    index = []
    p = re.compile(r'\d+')
    for i in range(len(s)):
        token = get_final_tokens(s[i])
        s[i] = ''
        for j in token:
            s[i] += j+' '
        if len(token) <5 and not p.search(s[i]):
            index.append(i)
    return index

csv_data = ReadCSVFile('../../info/1.csv')#读取文件
component = GetOneColumnData(csv_data,'Product Component')
description = GetOneColumnData(csv_data,'Description')
subject = GetOneColumnData(csv_data,'Subject')
resolution = GetOneColumnData(csv_data,'Resolution')
ReplaceCTXNumber(resolution)
bad_index = GetBadIndexInResolution(resolution)
for i in bad_index[::-1]:
    csv_data.pop(i)
print(len(bad_index))

with open('../../info/newcleandata.csv','w',newline='',encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Product Component','Subject','Description','Resolution'])
    for i in csv_data:
        writer.writerow(i)