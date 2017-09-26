#!python3
#-*-coding:utf-8-*-
import random
import matplotlib.pyplot as plt

def loadData(filename):
    d = []
    with open(filename,'r') as f:
        data = f.readlines()
    for x in data:
        p = x.strip().split()
        for n in range(len(p)):
            p[n] = float(p[n])
        d.append(p)
    return d

def kmeans(k,data):
    inter = 0
    l = len(data[0])
    max_min = getMax(data)
    point = getRandomPoint(k,max_min)#获得K个随机点
    for i in range(10):
        newData = fenlei(point,data)
        newPoint = getNewPoint(newData)
        point = newPoint
        # print('point'+str(i))
        # print(point)
    return point,newData

def getMax(data):
    l = len(data[0])
    v = []
    for x in range(l):
        v.append([0,0])
    for n in data:
        for m in range(l):
            if n[m]>v[m][1]:
                v[m][1] = n[m]
            elif n[m]<v[m][0]:
                v[m][0] = n[m]
    # print('v')
    # print(v)
    return v

def getRandomPoint(k,max_min):
    l = len(max_min)
    point=[]
    for i in range(k):
        one_point = []
        for j in range(l):
            r = random.uniform(max_min[j][0],max_min[j][1])
            # print('r')
            # print(r)
            one_point.append(r)
        point.append(one_point)
    # print('p')
    # print(point)
    return point

def fenlei(point,data):
    distance = {}
    newData=[]
    k = len(point)
    for i in range(k):
        distance[i] = 0
        newData.append([])
    for x in data:
        inter=0
        for y in point:
            d = 0
            for i in range(len(point[0])):
                d += (x[i]-y[i])**2
            distance[inter] = d
            inter+=1
        mindis = getTheMinDisInter(distance)
        newData[mindis].append(x)
    return newData

def getTheMinDisInter(distance):
    d=sorted(distance.items(),key=lambda item:item[1])
    return int(d[0][0])

def getNewPoint(newData):#newData=[[[1,2],[1,3]],[1,1]]]
    l = len(newData[0][0])
    k = len(newData[0])
    newPoint = []
    total = []
    for i in range(l):
        total.append(0)
    for m in newData:
        inter = 0
        np=[]
        for p in range(l):
            total[p]=0
        for n in m:
            inter+=1
            for p in range(l):
                total[p]+=n[p]
        print('total')
        print(total)
        for s in total:
            if inter == 0:
                np.append(0)
            else:
                np.append(s/inter)
        newPoint.append(np)
    print('newData')
    print(newData)
    print('newPoint')
    print(newPoint)
    return newPoint

x=loadData('testSet.txt')
p,d = kmeans(3,x)


fig = plt.figure()
color = ['red','blue','green']
inter=-1
for x in d:
    inter+=1
    for y in x:
        plt.scatter(y[0], y[1], color=color[inter])
inter=-1
for x in p:
    inter+=1
    plt.scatter(x[0], x[1], color=color[inter],marker='x')
plt.show()
