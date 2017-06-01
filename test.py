#!python3
#-*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
import time
import re
import pymongo
import random
from pymongo import MongoClient
import math
from sys import stdout


def getClient():
    try:
        client = MongoClient()
        return client
    except:
        print('连接指定集合失败！')
        return False

def closeClient(client):
    client.close()
#该函数接受希望保存进数据库的数据集（字典形式的）和一个name做该文档的_id。保存方式为save，意味着每次都会覆盖同意id的数据
def saveToMongodb(myclient,info,p_name,p_id):
    info['_id'] = p_id
    info['name'] = p_name
    db=myclient.test1
    collection=db.books2
    try:
        collection.save(info)
    except:
        print('保存进数据库失败')
        return False
    return True

def deleteDot(thelist):
    mylist={}
    for key in thelist.keys():
        mykey=key.replace('.','')
        mylist[mykey]=thelist[key]
    return mylist
book={'Node.js实战': 4, 'ES6 标准入门（第2版）': 4, '黑客与画家': 5, 'The Node Beginner Book': 5, '深入浅出Node.js': 4, '解忧杂货店': 5, '幻夜': 4, 'JavaScript忍者秘籍': 4, 'JavaScript设计模式与开发实践': 5, '你不知道的JavaScript（上卷）': 5, '高性能JavaScript': 5, 'JavaScript权威指南(第6版)': 4, 'JavaScript语言精粹': 5, 'AngularJS权威教程': 4, '用AngularJS开发下一代Web应用': 3, 'JavaScript高级程序设计（第3版）': 5, 'Head First HTML与CSS、XHTML（中文版）': 4, 'Java编程思想 （第4版）': 5, '算法导论（原书第3版）': 5, '变身': 3, '秘密': 4, '达芬奇密码': 4, '白夜行': 5, '嫌疑人X的献身': 5, '三体Ⅱ': 5, '三体Ⅲ': 5, '我就是想停下来，看看这个世界': 3, '魔力': 3, '侠客行（全二册）': 4, '平凡的世界': 5, '雷雨': 4, '梦里花落知多少': 5, '死魂灵': 4, '杰克·伦敦小说选': 4, '基督山伯爵': 5, '羊脂球': 5, '名人传': 4, '了不起的盖茨比': 4, '格列佛游记': 4, '汤姆・索亚历险记': 4, '莫泊桑短篇小说选': 5, '伊索寓言': 4, '爱伦·坡短篇小说集': 5, '威尼斯商人': 4, '变形记': 3, '爱的教育': 4, '百年孤独': 5, '假如给我三天光明': 4, '爱伦·坡暗黑故事全集（上册）': 5, '少年维特的烦恼': 4, '欧·亨利短篇小说选': 5, '雾都孤儿': 4, '项链': 5, '在路上': 3, '一千零一夜': 4, '洛丽塔': 4, '瓦尔登湖': 5, '肖申克的救赎': 5, '像少年啦飞驰': 4, '一座城池': 4, '悟空传': 5, '何以笙箫默': 3, '岛': 4, '围城': 5, '不能承受的生命之轻': 5, '挪威的森林': 5, '货币战争': 3, '麦田里的守望者': 5, '达·芬奇密码': 4, '小王子': 4, '世界因你不同': 4, '安徒生童话故事集': 5, '三国演义（全二册）': 5, '致我们终将逝去的青春': 3, '独唱团（第一辑）': 4, '飘': 5, '人生': 5, '藏海花': 5, '三体': 5, '苏菲的世界': 5, '史蒂夫·乔布斯传': 5, '水浒传（全二册）': 5, '明朝那些事儿（柒）：大结局': 5, '幽游白书（全19册）': 5, '盗墓笔记3': 5, '明朝那些事儿（伍）': 5, '明朝那些事儿（1-9）': 5, '麦琪的礼物': 5, '海贼王': 5, '明朝那些事儿（肆）': 5, '钢铁是怎样炼成的': 5, '鲁滨逊漂流记': 5, '明朝那些事儿（贰）': 5, '老人与海': 5, '活着': 4, '明朝那些事儿（陆）': 5, '盗墓笔记4': 5, '谁动了我的奶酪？': 4, '盗墓笔记2': 5, '格林童话全集': 5, '明朝那些事儿（叁）': 5, '盗墓笔记': 5, '小时代1.0折纸时代': 1, '边城': 5, '天龙八部': 5, '看见': 5, '明朝那些事儿（壹）': 5, '三重门': 5}

# c = getClient()
# saveToMongodb(c,i,'吴凡','12345456')
# closeClient(c)
a = deleteDot(book)
print(a)
