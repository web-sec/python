import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn import svm

#df = pd.read_excel("info/printing.xlsx",sheet_name="Sheet1")
df = pd.read_csv("../info/all.csv",nrows=10000)
problem_types = df['ProblemType']
description = df['Description']
nan = float('nan')
for i in range(len(problem_types)-1,-1,-1):
    if type(description[i]) == type(nan):
        del (description[i])
        del (problem_types[i])

# vectorizer=CountVectorizer(stop_words='english')#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
# transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值
# tfidf=transformer.fit_transform(vectorizer.fit_transform(description))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵


#打印出每个文档的TF-IDF
# word=vectorizer.get_feature_names()#获取词袋模型中的所有词语
# weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
# for i in range(len(weight)):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
#     print("-------这里输出第{index}个描述的tf-idf-------".format(index=i))
#     for j in range(len(word)):
#         if weight[i][j] !=0:
#             print(word[j],weight[i][j])

#统计一共有哪些问题类型
# def GetAllKendOfTypes(problem_types):
#     types = []
#     for x in problem_types:
#         if x not in types:
#             types.append(x)
#     return types

types = []
for x in problem_types:
    if x == 'Configuration':
        types.append(1)
    else:
        types.append(0)

vectorizer = TfidfVectorizer(min_df = 0.0,sublinear_tf=True,stop_words='english',ngram_range=(1,1))
X = vectorizer.fit_transform(description)#计算每个词语的tf-idf权值

# vectorizer=CountVectorizer(stop_words='english')#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
# transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值
# X=transformer.fit_transform(vectorizer.fit_transform(description))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
# word=vectorizer.get_feature_names()#获取词袋模型中的所有词语

y = types
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
clf = svm.SVC(C=2,kernel='linear')
clf.fit(X_train,y_train)
predicted = clf.predict(X_test)

print(metrics.accuracy_score(y_test,predicted))
print(metrics.precision_score(y_test,predicted))
print(metrics.recall_score(y_test,predicted))
print(metrics.f1_score(y_test,predicted))
