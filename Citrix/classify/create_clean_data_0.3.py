#coding:utf-8
import nltk
from nltk.stem.porter import *
import csv
import string
from nltk.corpus import stopwords
from collections import Counter
noenglish = 0
nolegalcomp = 0
ctxdata = 0
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
            if not IsIllegalData(i):
                data.append(i)
    print('has read {length} data.'.format(length=len(data)))
    return data

#获取指定列名的全部信息；
def GetOneColumnData(source,column_name):
    column_list = source[0]
    print(column_list)
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

def NotEnglish(string):
    for c in string:
        if ord(c) > 128:
            return True
    return False

def ResolutionIsIlleagal(s):
    rule = re.compile(r'http.*CTX\d*')#形如'http://support.citrix.com/article/CTX138195'的文本
    if len(get_final_tokens(s)) < 5 or rule.search(s):
        return True


def IsIllegalData(one_piece_of_data):
    l = len(one_piece_of_data)
    if l < 14:
        return True
    else:
        illegal_data = ['No Applicable Component','Unspecified','Desktop VDA','Server VDA' ,'n/a' ,'N/A']
        for i in [7,10,11,12]:
            if one_piece_of_data[i] in illegal_data or NotEnglish(one_piece_of_data[i]):
                return True
            #elif ComponentIsIlleagal(one_piece_of_data[7]):
            #elif SubjectIsIlleagal(one_piece_of_data[10]):
            #elif DescriptionIsIlleagal(one_piece_of_data[11]):
            #elif ResolutionIsIlleagal(one_piece_of_data[12]):
            #    return True
    return False

csv_data = ReadCSVFile('../../info/all.csv')#读取文件
case_id = GetOneColumnData(csv_data,'Id')
case_number = GetOneColumnData(csv_data,'CaseNumber')
component = GetOneColumnData(csv_data,'Product Component')
description = GetOneColumnData(csv_data,'Description')
subject = GetOneColumnData(csv_data,'Subject')
resolution = GetOneColumnData(csv_data,'Resolution')
print(len(component),len(description),len(subject),len(resolution))


with open('../../info/newcleandata.csv','w',newline='',encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Product Component','Subject','Description','Resolution'])
    for i,j,x,y,z,p in zip(case_id,case_number,component,subject,description,resolution):
        writer.writerow([i,j,x,y,z,p])