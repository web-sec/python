# -*- coding: utf-8 -*-

from numpy import *


def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]


# C1 是大小为1的所有候选项集的集合
def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])  # store all the item unrepeatly

    C1.sort()
    # return map(frozenset, C1)#frozen set, user can't change it.
    return list(map(frozenset, C1))


# 该函数用于从 C1 生成 L1 。
def scanD(D, Ck, minSupport):
    # 参数：数据集、候选项集列表 Ck以及感兴趣项集的最小支持度 minSupport
    ssCnt = {}
    for tid in D:  # 遍历数据集
        for can in Ck:  # 遍历候选项
            if can.issubset(tid):  # 判断候选项中是否含数据集的各项 set数据的内建方法a.set(b)：判断集合a是否是集合b的子集
                # if not ssCnt.has_key(can): # python3 can not support
                if not can in ssCnt:
                    ssCnt[can] = 1  # 不含设为1
                else:
                    ssCnt[can] += 1  # 有则计数加1
    numItems = float(len(D))  # 数据集大小
    retList = []  # L1 保存满足最小支持度的候选项
    supportData = {}  # 记录候选项中各个数据的支持度
    for key in ssCnt:
        support = ssCnt[key] / numItems  # 计算支持度
        if support >= minSupport:
            retList.insert(0, key)  # 满足条件加入L1中
        supportData[key] = support
    return retList, supportData


# total apriori
def aprioriGen(Lk, k):  # 组合，向上合并
    # creates Ck 参数：频繁项集列表 Lk 与项集元素个数 k
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):  # 两两组合遍历
            L1 = list(Lk[i])[:k - 2]
            L2 = list(Lk[j])[:k - 2]
            L1.sort()
            L2.sort()
            if L1 == L2:  # 若两个集合的前k-2个项相同时,则将两个集合合并
                retList.append(Lk[i] | Lk[j])  # set union
    return retList


# apriori
def apriori(dataSet, minSupport=0.5):
    C1 = createC1(dataSet)  # 获得候选项集（此处为二维列表中非重复数字）
    D = list(map(set, dataSet))  # python3 令dataSet中每个子数据都变为set类型
    L1, supportData = scanD(D, C1, minSupport)  # 单项最小支持度判断 0.5，生成L1；
    # l1是满足最小支持度的候选项列表；supportData是记录候选项中各个数据的支持度的字典
    L = [L1]
    k = 2
    while (len(L[k - 2]) > 0):  # 创建包含更大项集的更大列表,直到下一个大的项集为空
        Ck = aprioriGen(L[k - 2], k)  # Ck
        Lk, supK = scanD(D, Ck, minSupport)  # get Lk
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData

print(apriori(loadDataSet()))