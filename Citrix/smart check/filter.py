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


with open('data.txt','r',encoding='utf-8') as f :
    data = f.readlines()


rule1 = re.compile(r'\d{3}')
rule2 = re.compile(r'http')
rule3 = re.compile(r'ctx')
rule4 = re.compile(r'program files')
rule5 = re.compile(r'<-->')
rule6 = re.compile(r'=>')
rule7 = re.compile(r'>>')
rule8 = re.compile(r'c:')

rules = [rule1,rule2,rule3,rule4,rule5,rule6,rule7,rule8]
d=[]
n=0
for i in data:
    flag=0
    s=''
    token = get_simple_tokens(i)
    if len(token)>=20:
        n+=1
        s = i.lower()
        for rule in rules:
            if rule.search(s):
                flag+=1
        print(flag)
        if flag==0:
            d.append(i)
print(len(d))
print(n)
with open('a.txt','w',encoding='utf-8') as f:
    f.writelines(d)