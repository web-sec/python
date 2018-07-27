#coding:utf-8
import gensim
import a
import nltk
import string
import csv

def get_simple_tokens(text):#对文章进行分词
    lowers = text.lower()
    #remove the punctuation using the character deletion step of translate
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)#ord()函数返回对应字符的ASCLL值
    no_punctuation = lowers.translate(remove_punctuation_map)#字符串的translate()方法将原字符串的指定字符替换成别的指定字符
    tokens = nltk.word_tokenize(no_punctuation)#可能需要手动下载某数据包，看报错即可
    return tokens

def WriteTrainDataToCsv(csv_path,data):
    #写入训练后的测试数据
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for i in data:
            writer.writerow(i)

model = gensim.models.Word2Vec.load('DR_model')
description = a.description
X = []
for i in description:
    vec = [0 for i in range(300)]
    clean_i = get_simple_tokens(i)
    for w in clean_i:
        try:
            w_vec = model[w]
        except:
            w_vec = [0 for i in range(300)]
        for n in range(300):
            vec[n]+=w_vec[n]
    X.append(vec)
    print(len(X))
WriteTrainDataToCsv('DR_model_300.csv',X)

