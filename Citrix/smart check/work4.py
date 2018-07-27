# coding:utf-8
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
def ReadCSVFile(filepath, encoding='utf-8'):
    data = []
    with open(filepath, 'r', encoding=encoding) as f:
        reader = csv.reader((line.replace('\0', '') for line in f))
        for i in reader:
            data.append(i)
    return data

newdata=[]
data = ReadCSVFile('mydata2.csv')
n=0
for i in data:
    n+=1
    if n%100==0:
        print(n)
    issue = i[3]
    case = i[10]
    if abs(len(issue)-len(case))/len(case)<0.2:
        for j in case:
            if ord(j)<127:
                token1 = get_final_tokens(issue)
                token2 = get_final_tokens(case)
                same = len([val for val in token1 if val in token2])
                if same/len(token1) > 0.5:
                    print(i)
                    newdata.append(i)


with open('mydata4.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    # writer.writerow(['Product Component','Subject','Description','Resolution'])
    for x in newdata:
        writer.writerow(x)