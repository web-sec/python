#!/usr/bin/python
#-*-coding:utf-8-*-
from math import sqrt

critics={'zhangsan':{'Lady in the Water':2.5,'Snakes on a Plane':3.5,'Just My Luck':3.0,'Superman Returns':3.5,'you,Me and Dupree':2.5,'The Night Listerner':3.0},
'lisi':{'Lady in the Water':3.0,'Snakes on a Plane':3.5,'Just My Luck':1.5,'Superman Returns':5.0,'you,Me and Dupree':3.0,'The Night Listerner':3.5},
'wangwu':{'Lady in the Water':2.5,'Snakes on a Plane':3.0,'Superman Returns':3.5,'The Night Listerner':4.0},
'tom':{'Snakes on a Plane':3.5,'Just My Luck':3.0,'Superman Returns':4.0,'you,Me and Dupree':2.5,'The Night Listerner':4.5},
'jack':{'Lady in the Water':3.0,'Snakes on a Plane':4.0,'Just My Luck':2.0,'Superman Returns':3.0,'you,Me and Dupree':2.0,'The Night Listerner':3.0},
'harry':{'Lady in the Water':3.0,'Snakes on a Plane':4.0,'Superman Returns':5.0,'you,Me and Dupree':3.5,'The Night Listerner':3.0},
'ben':{'Snakes on a Plane':4.5,'Superman Returns':4.0,'you,Me and Dupree':1.0}}

#计算两人之间的欧几里得距离
def sim_euclidean(prefs,person1,person2):
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1;
    if len(si)==0:return 0
    sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2)for item in prefs[person1] if item in prefs[person2]])
    return 1/(1+sqrt(sum_of_squares))

#安从高到低的顺序返回指定数量的两两之间的欧几里得/皮尔逊距离
def carculate(number,func):
    mylist={}
    for p1 in critics:
        for p2 in critics:
            if p1!=p2:
                mylist.update({p1+' and '+p2+' '+func.__name__:round(func(critics,p1,p2),4)})
    mylist_sorted=sorted(mylist.items(),key=lambda mylist:mylist[1],reverse=True)
    #sorted(iterable,key,reverse)方法返回一个排序号的列表，
    #items()方法将字典的元素转化为了元组，而这里key参数对应的lambda表达式的意思则是选取元组中的第二个元素作为比较参数
    #reverse控制排序的方式:true代表从大到小，默认是从小到大
    for i in range(number):
        print(mylist_sorted[i*2+1])
    #按上面的算法会产生a与b和b与a的重复，所以这里只取单数的
    #python里字符串与数字不能呢个直接拼接，要用str()将数字转换成字符串

#该函数返回指定两者的皮尔逊系数
def sim_pearson(prefs,p1,p2):
    si={}
    for item in prefs[p1]:
        if item in prefs[p2]:si[item]=1

    n=len(si)
    if n==0:return 1
    # 对所有偏好求和
    sum1=sum([prefs[p1][it] for it in si])
    sum2=sum([prefs[p2][it] for it in si])
    #求平方和
    sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq=sum([pow(prefs[p2][it],2) for it in si])
    #求乘积之和
    pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])
    #计算皮尔逊价值
    num=pSum-(sum1*sum2/n)
    den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if den==0:return 0

    r=num/den
    return r

def getRecommendations(prefs,person,similarity=sim_pearson):
    totals={}
    simSums={}
    for other in prefs:
        if other==person:continue
        sim=similarity(prefs,person,other)

        if sim<=0:continue
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item]==0:
                totals.setdefault(item,0)#dict.setdefault(key,[default])如果键在字典中，返回这个键所对应的值。如果键不在字典中，向字典 中插入这个键，并且以default为这个键的值，并返回 default。default的默认值为None
                totals[item]+=prefs[other][item]*sim
                simSums.setdefault(item,0)
                simSums[item]+=sim
    #建立一个归一化的列表
    rankings=[(total/simSums[item],item) for item,total in totals.items()]#totals.items()方法将字典转变为元组
    #返回进过排序的列表
    rankings.sort()
    rankings.reverse()#反向排序
    return rankings

#从反映偏好的字典中返回最佳匹配者
def topMatches(prefs,person,n=5,similarity=sim_pearson):
  scores=[(similarity(prefs,person,other),other)
  for other in prefs if other!=person]
  scores.sort()
  scores.reverse()
  return scores[0:n]

def transformPrefs(prefs):
  result={}
  for person in prefs:
    for item in prefs[person]:
      result.setdefault(item,{})

      #将物品和人员对调
      result[item][person]=prefs[person][item]
  return result

def calculateSimilarItems(prefs,n=10):
  #给出与这些物品最接近的所有物品
  result={}
  #以物品为中心对偏好矩阵实施倒置处理
  itemPrefs=transformPrefs(prefs)
  c=0
  for item in itemPrefs:
    c+=1
    if c%100==0: print "%d / %d" % (c,len(itemPrefs))
    #寻找最为相近的物品
    scores=topMatches(itemPrefs,item,n=n,similarity=sim_euclidean)
    result[item]=scores
  return result

def getRecommendedItems(prefs,itemMatch,user):
  userRatings=prefs[user]
  scores={}
  totalSim={}
  #循环遍历由当前用户评分的物品
  for (item,rating) in userRatings.items( ):

    #循环遍历与当前物品相近的物品
    for (similarity,item2) in itemMatch[item]:

      if item2 in userRatings: continue
      #评价值与相似度的加权之和
      scores.setdefault(item2,0)
      scores[item2]+=similarity*rating
      #全部相似度之和
      totalSim.setdefault(item2,0)
      totalSim[item2]+=similarity

  #将每个合计值除以加权和，求出平均值
  rankings=[(score/totalSim[item],item) for item,score in scores.items( )]

  #案由高到低排序
  rankings.sort( )
  rankings.reverse( )
  return rankings

if __name__ == '__main__':
    # carculate(10,sim_euclidean)
    # carculate(10,sim_pearson)
    # print(getRecommendations(critics,'tom'))
    itemsim=calculateSimilarItems(critics)
    print(getRecommendedItems(critics,itemsim,'harry'))
