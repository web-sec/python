#coding:utf-8
import nltk
from nltk.stem.porter import *
import csv
import string
from nltk.corpus import stopwords
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

def NotEnglish(string):
    for c in string:
        if ord(c) > 128:
            return True
    return False

def ResolutionIsIlleagal(s):
    flag=0
    rule = re.compile(r'http.*CTX\d*')#形如'http://support.citrix.com/article/CTX138195'的文本
    if len(get_final_tokens(s))<5:
        short_resolution+=1
        flag+=1
    if  rule.search(s):
        ctx_data+=1
        flag+=1
    if flag>0:
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
            elif ResolutionIsIlleagal(one_piece_of_data[12]):
                return True
    return False

n=0
m=0
data=[]
a=0
b=0
c=0
d=0
e=0
csv_data = ReadCSVFile('../../info/after_token.csv')#读取文件

for i in csv_data[::-1]:
    if i[12].strip() == 'na' or i[12].strip() == 'unspecifi':
        csv_data.remove(i)
        n+=1
        print(n)
with open('../../info/newcleandata.csv','w',newline='',encoding='utf-8') as f:
    writer = csv.writer(f)
    for i in csv_data:
        writer.writerow(i)