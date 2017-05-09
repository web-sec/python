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
def sim_distance(prefs,person1,person2):
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1;
    if len(si)==0:return 0
    sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2)for item in prefs[person1] if item in prefs[person2]])
    return 1/(1+sqrt(sum_of_squares))

#安从高到低的顺序返回指定数量的两两之间的欧几里得距离
def euclidean(number):
    mylist={}
    for p1 in critics:
        for p2 in critics:
            if p1!=p2:
                mylist.update({p1+' and '+p2:round(sim_distance(critics,p1,p2),4)})
    mylist_sorted=sorted(mylist.items(),key=lambda mylist:mylist[1],reverse=True)
    #sorted(iterable,key,reverse)方法返回一个排序号的列表，
    #items()方法将字典的元素转化为了元组，而这里key参数对应的lambda表达式的意思则是选取元组中的第二个元素作为比较参数
    #reverse控制排序的方式:true代表从大到小，默认是从小到大
    for i in range(number):
        print(mylist_sorted[i*2+1])
    #按上面的算法会产生a与b和b与a的重复，所以这里只取单数的
    #python里字符串与数字不能呢个直接拼接，要用str()将数字转换成字符串


euclidean(10)
