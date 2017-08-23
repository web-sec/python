#!python3
#-*-coding:utf-8-*-
from pymongo import MongoClient

def getNameIDFromDB():
    name_id = {}
    myclient = MongoClient('mongodb://localhost')
    mycollection = myclient['music']['peopleinfo']
    cursor = mycollection.find({'iscrawlered':1})
    for x in cursor:
        name_id.update({x['name']:x['id']})
    myclient.close()
    return name_id

def getMusicFromDB():
    music = {}
    name_id = getNameIDFromDB()
    myclient = MongoClient('mongodb://localhost')
    mydb = myclient['music']
    for name in name_id:
        mycollection = mydb[name]
        cursor = mycollection.find_one()
        music_list = cursor['music']
        music.update({name:music_list})
    return music

def searchSameMusic(music):
    result = {}
    music_shenyizhou = music['一只大汪呜']
    music.pop('一只大汪呜')
    for name,music_list in music.items():
        result.update({name:calculation2(music_shenyizhou,music_list)})
    return result

def calculation1(list1,list2):
    score = 0
    for m in list1:
        for n in list2:
            if m == n:
                score+=1
    return score

def calculation2(list1,list2):
    score = 0
    for m in list1:
        for n in list2:
            if m == n:
                score+=1
    score2 = score/len(list1)+score/(len(list2)+1)
    return round(score2,3)


music = getMusicFromDB()
result = searchSameMusic(music)
result = sorted(result.items(),key=lambda item:item[1],reverse=True)
print(result)
