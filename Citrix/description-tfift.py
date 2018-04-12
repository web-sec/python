#coding:utf-8
import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import csv
# df = pd.read_csv("info/all.csv")
# description = df['Description']
data = []
with open('../info/all.csv','r',encoding='utf-8') as f:
    reader = csv.reader(f)
    for i in reader:
        data.append(i)
description = []
for i in data[1:10000]:
    description.append(i[11])
print(len(description))

# print(description[0])
# print(len(description))
vectorizer=CountVectorizer(stop_words='english')#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值
tfidf=transformer.fit_transform(vectorizer.fit_transform(description))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵

#打印出每个文档的TF-IDF
word=vectorizer.get_feature_names()#获取词袋模型中的所有词语
weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
for i in range(25):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
    print("-------这里输出第{index}个描述的tf-idf-------".format(index=i))
    for j in range(len(word)):
        if weight[i][j] !=0:
            print(word[j],weight[i][j])

# keywords = []
# for i in range(len(weight)):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
#     #print("-------这里输出第{index}个描述的tf-idf-------".format(index=i))
#     max_index = 0
#     max = 0
#     for j in range(len(word)):
#         if weight[i][j] > max:
#             max_index = j
#             max = weight[i][j]
#     #print(word[max_index],max)
#     keywords.append({word[max_index]:max})

# print(keywords)