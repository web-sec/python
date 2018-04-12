import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

def DeleteNan(s1,s2):
    nan = float('nan')
    amount = 0
    for i in range(len(s1)-1,-1,-1):
        if type(s2[i]) == type(nan):
            amount += 1
            del (s2[i])
            del (s1[i])
    print('delete {amount} nan text'.format(amount=amount))
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

def SelectType(problem_type,typename):
    types = []
    for x in problem_type:
        if x == typename:
            types.append(1)
        else:
            types.append(0)
    return types



df = pd.read_csv("../info/all.csv", nrows=10000)
problem_types = df['ProblemType']
description = df['Description']

DeleteNan(problem_types,description)
#all kind of types are:
# 'Configuration', 'Installation / Upgrade', 'Performance',
# 'No Applicable Problem Type', 'How-to / General Question',
# 'Bug / Defect', '3rd Party / Compatibility', 'Crash / Hang',
# 'Unspecified', 'Documentation', 'Other', 'HA / Load Balancing', 'Enhancement Request'
type = 'Configuration'
types = SelectType(problem_types,type)

vectorizer = TfidfVectorizer(stop_words = 'english')
X = vectorizer.fit_transform(description)#计算每个词语的tf-idf权值
print(X)
# vectorizer=CountVectorizer(stop_words='english')#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
# transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值
# X=transformer.fit_transform(vectorizer.fit_transform(description))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
# word=vectorizer.get_feature_names()#获取词袋模型中的所有词语

y = types
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
lgs = LogisticRegression(penalty='l2', class_weight='balanced')
lgs.fit(X_train, y_train)
predicted = lgs.predict(X_test)

accuracy = metrics.accuracy_score(y_test,predicted)
precision = metrics.precision_score(y_test,predicted)
recall = metrics.recall_score(y_test,predicted)
f1 = metrics.f1_score(y_test,predicted)
print('types:'+type)
print('accuracy: {accuracy}'.format(accuracy=accuracy))
print('precision: {precision}'.format(precision=precision))
print('recall: {recall}'.format(recall=recall))
print('f1: {f1}'.format(f1=f1))
feature = lgs.coef_[0]
print('feature quantity: {quantity}'.format(quantity=len(feature)))