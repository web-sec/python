#!python3
#-*-coding:utf-8-*-
from numpy import *
import operator

def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group,labels

def classify0(inx,dataSet,labels,k):#(待分类向量inx,训练样本dataSet,样本标签向量labels,最近邻数k)
    distance = []
    l = []
    p = {}
    for x in dataSet:
        distance.append(jisuan(inx,x))
    for (a,b) in zip(distance,labels):
        l.append([a,b])
    l = sorted(l,key=operator.itemgetter(0),reverse=False)
    for n in range(k-1):
        p[l[n][1]]=0
    for n in range(k-1):
        for x in p.keys():
            if l[n][1]==x:
                p[x]+=1
    m = max(p, key=p.get)
    print(l)
    return m

def jisuan(list1,list2):
    result = 0
    for (x,y) in zip(list1,list2):
        result += (y-x)**2
    return result**0.5

group,labels = createDataSet()
p = {'a':1,'b':2,'c':3}
print(max(p))
