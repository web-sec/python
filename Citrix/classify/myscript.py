import urllib.parse
import os
import numpy as np
from sklearn import svm
# from sklearn.model_selection import GridSearchCV
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.externals import joblib

def loadFile(name):
    directory = str(os.getcwd())
    filepath = os.path.join(directory, name)
    with open(filepath,'r') as f:
        data = f.readlines()
    data = list(set(data))
    result = []
    for d in data:
        d = str(urllib.parse.unquote(d))   #converting url encoded data to simple string
        result.append(d)
    return result


badQueries = loadFile('badqueries.txt')
validQueries = loadFile('goodqueries.txt')
# badQueries = loadFile('bad.txt')#读文件
# validQueries = loadFile('good.txt')

testQueries = loadFile('test.txt')
#print(len(testQueries))

badQueries = list(set(badQueries))#去重
badQueries = badQueries[:40000]
validQueries = list(set(validQueries))
validQueries = validQueries[:80000]
testQueries = list(set(testQueries))
allQueries = badQueries + validQueries

yBad = [1 for i in range(0, len(badQueries))]  #[1,1,1...]
yGood = [0 for i in range(0, len(validQueries))]#[0,0,0...]
y = yBad + yGood

queries = allQueries


vectorizer = TfidfVectorizer(min_df = 0.0,analyzer='char',sublinear_tf=True,ngram_range=(1, 3)) #初始化,该类会统计每个词语的tf-idf权值
    #min_df:临界值
    #analyzer:特征是否应当由单词或n-gram构成
    #sublinear_tf：是否应用线性tf缩放（用1+log(tf)取代tf）
    #ngram_range:n-gram中第n个词的出现只与前面N-1个词相关

#querys是样本文档
#testQuerys是新文档
vectorizer.fit(queries)
X = vectorizer.transform(queries)#计算每个词语的tf-idf权值
T = vectorizer.transform(testQueries)
# print(len(X.toarray()[0]))
# print(len(T.toarray()[0]))
# print(len(vectorizer.get_feature_names()))
# print(len(X.toarray()[0]))
# word = vectorizer.get_feature_names()
# weight = X.toarray()
#
# for i in range(len(weight)):
#     print(queries[i])
#     print('-------------------------------------')
#     for j in range(len(word)):
#         if weight[i][j] != 0.0:
#             print(word[j],weight[i][j])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) #splitting data
    #train_test_split（）：快速地将数据划分为训练集合与测试结合。从样本中随机的按比例选取train data和testdata
    #cross_validation.train_test_split(train_data,train_target,test_size=0.4, random_state=0)
    # 参数解释：
    # train_data：所要划分的样本特征集
    # train_target：所要划分的样本结果
    # test_size：样本占比，快速的采样到一个训练集合同时保留 40% 的数据用于测试（评估）我们的分类器
    # random_state：是随机数的种子。
# print('******************************************************')
# print(len(X_train.toarray()[0]))
# print('******************************************************')
# print(len(X_test.toarray()[0]))
# print('------------------------------------')
# print(X_train)
# print('------------------------------------')
# print(y_train)

badCount = len(badQueries)
validCount = len(validQueries)

t1 = time.time()

lgs = LogisticRegression(penalty='l2', class_weight={1: 2 * validCount / badCount, 0: 1.0}) # class_weight='balanced')
    #class sklearn.linear_model.LogisticRegression(penalty='l2', dual=False, tol=0.0001, C=1.0, fit_intercept=True, intercept_scaling=1, class_weight=None, random_state=None, solver='liblinear', max_iter=100, multi_class='ovr', verbose=0, warm_start=False, n_jobs=1)
    #class_weight参数用于标示分类模型中各种类型的权重
    #LogisticRegression.coef_存放回归系数，LogisticRegression.intercept_则存放截距

#-----------------------svm----------------------------
# clf = svm.SVC(C=0.5,kernel='linear')
# clf.fit(X_train,y_train)
# p = clf.predict(T)
# predicted = clf.predict(X_test)
# p1 = [1 for i in range(50)]
# p2 = [0 for i in range(50)]
# py = p1+p2
#
# print(p[:50])
# print(p[50:])
# print(metrics.f1_score(y_test,predicted))
# print(metrics.f1_score(py,p))

#---------------------------------------

lgs.fit(X_train, y_train) #训练
t2 = time.time()

# print(lgs.coef_)
# print(T.toarray())
#print(lgs.score(X_test,y_test))
#
# for i in range(len(T.toarray())):
#     p=0
#     for x in range(len(lgs.coef_[0])):
#         p+=T.toarray()[i][x]*lgs.coef_[0][x]
#     print(p)

predicted = lgs.predict(X_test)#对测试集的预测,结果为0，1矩阵
#print(len(predicted))

#p = lgs.predict(T)#对新文本的分类预测
#print(p[:10])
#print(p[10:])
# p1 = [1 for i in range(10)]
# p2 = [0 for i in range(10)]
# py = p1+p2
print(metrics.accuracy_score(y_test,predicted))
print(metrics.precision_score(y_test,predicted))
print(metrics.recall_score(y_test,predicted))
print(metrics.f1_score(y_test,predicted))
print(t2-t1)
#print(metrics.f1_score(py,p))
# n=0
# for x in range(len(predicted)):
#     if predicted[x] == y_test[x]:
#         n+=1
# print(len(predicted))
# print(n)
#
# fpr, tpr, _ = metrics.roc_curve(y_test, (lgs.predict_proba(X_test)[:, 1]))
#  #计算roc曲线的假阳性率、真阳性率、阈值
#  #sklearn.metrics.roc_curve(y_true, y_score, pos_label=None, sample_weight=None, drop_intermediate=True)[source]
#  #predict_proba（）：计算测试样本属于各个类别的概率
#  #x[:,1] :取x矩阵的第二列数据，返回一个列表
#
# auc = metrics.auc(fpr, tpr)
#  #计算roc曲线下的面积
# print(auc)
# f1 = metrics.f1_score(y_test,predicted)
# print(f1)
#
# time2 = time.time()
# print(time2-time1)
# # print("Bad samples: %d" % badCount)
# # print("Good samples: %d" % validCount)
# # print("Baseline Constant negative: %.6f" % (validCount / (validCount + badCount)))
# # print("------------")
# # print("Accuracy: %f" % lgs.score(X_test, y_test))  #checking the accuracy
# # print("Precision: %f" % metrics.precision_score(y_test, predicted))
# # print("Recall: %f" % metrics.recall_score(y_test, predicted))
# # print("F1-Score: %f" % metrics.f1_score(y_test, predicted))
# # print("AUC: %f" % auc)
# # plt.title('Receiver Operating Characteristic')
# # plt.plot(fpr, tpr, 'b', label='AUC = %0.2f' % auc)
# # plt.legend(loc='lower right')
# # plt.plot([0,1],[0,1],'r--')
# # plt.xlim([0.0,1.0])
# # plt.ylim([0.0,1.0])
# # plt.ylabel('Recall')
# # plt.xlabel('Fall-out')
# # plt.show()