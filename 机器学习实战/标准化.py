#*-coding:utf-8-*
#0均值标准化(Z-score standardization) xi = (xi-E/SD)
from __future__ import division #py2.x需要，py3自带
def ZSN(numlist):
    newlist = []
    E = Expect(numlist)
    print('期望：'+str(E))
    SD = StandardDeviation(numlist)
    print('方差:'+str(SD))
    for i in numlist:
        newlist.append((i-E)/SD)
    return newlist

#线性函数归一化(Min-Max scaling) xi = (xi-xmin)/(xmax-xmin)
def MinMaxScaling(numlist):
    newlist = []
    Max = max(numlist)
    Min = min(numlist)
    for i in numlist:
        newlist.append((i-Min)/(Max-Min))
    return newlist
#计算平均值（期望）
def Expect(numlist):
    E = sum(numlist)/len(numlist)
    return E

#计算方差
def StandardDeviation(numlist):
    variance = 0
    E = Expect(numlist)
    for i in numlist:
        variance += (i-E)**2
    SD = variance/len(numlist)
    return SD



a=[23,21,54,67,7,99,15,32]
b=MinMaxScaling(a)
print(b)
