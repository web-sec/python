#!python3
#-*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
import time
import re
import pymongo
import random
from pymongo import MongoClient

url = "https://book.douban.com/people/john91/collect"
cookies = {'cookie':'ll="118159"; bid=rIFKNErGPjM; viewed="2042063"; gr_user_id=6302343c-4d52-4903-86d3-72e66cd99228; ps=y; ue="495464616@qq.com"; __ads_session=ggwUaKo46gjw+v8AIAA=; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=6521c349-5966-4355-847a-a67548809e6a; gr_cs1_6521c349-5966-4355-847a-a67548809e6a=user_id%3A1; __utmt_douban=1; __utma=30149280.886896177.1484292481.1495594251.1495676585.6; __utmb=30149280.1.10.1495676585; __utmc=30149280; __utmz=30149280.1495676585.6.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _vwo_uuid_v2=B5D7C7975C5D7F6241ADD9533A376ABA|50e0f527e7cb50ccd1ec80fde50abfcf; push_noty_num=0; push_doumail_num=0; ap=1; as="https://book.douban.com/"'}
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

def getHtmlData(url,cookies,headers):
    try:
        r = requests.get(url,cookies=cookies,headers=headers)
        r.encoding = 'utf-8'
        content = r.text
    except:
        print('get '+url+' failed!')
    return content

#该函数返回指定页面每本书的评价，返回一个{‘书名’：评价分}的字典
def getBooksMarking(content):
    booknames = []
    bookscores = []
    evaluatioin = {}
    soup = BeautifulSoup(content,'lxml')
    booklist_a = soup.select('.article > ul > li > .info > h2 > a')
    booklist_span = soup.select('.article > ul > li > .info > .short-note > div > span:nth-of-type(1)')
    for book in booklist_a:
        booknames.append(book.attrs['title'])#booknames列表存储了当前页面所有书的名字，形式为['乌合之众', '菊与刀', '孟子趣说3', '孟子趣说2', '孟子趣说1', '逍遥游', '我们为什么离正义越来越远', '中国思想地图', '《理想国》讲演录', '春秋大义', '理想国', '且介亭杂文末编', '且介亭杂文二集', '现象学导论', '且介亭杂文']
    for book in booklist_span:
        bookscores.append(book.attrs['class'])#bookscores列表存储了当前页面书本的评分，形式为[['rating4-t'], ['rating4-t'], ['rating4-t'], ['rating4-t'], ['rating4-t'], ['rating4-t'], ['rating5-t'], ['rating4-t'], ['rating4-t'], ['rating4-t'], ['rating5-t'], ['rating4-t'], ['rating4-t'], ['rating4-t'], ['rating4-t']]
    score_list = getbookScores(bookscores)
    if len(booknames) == len(score_list):
        for index in range(0,len(booknames)):
            evaluatioin[booknames[index]]=score_list[index]
    else:
        print('长度不相匹配，出问题了!')
    return evaluatioin

#该函数处理一下爬取到的书本评价分，以列表形式返回每本书的评价分，元素为int型
def getbookScores(scorelist):
    empty_list1 = []
    empty_list2 = []
    score_list = []
    mode = re.compile(r'\d+')
    for onebookscore in scorelist:#去除中括号
        empty_list1.append(onebookscore[0])
    for onebookscore in empty_list1:#正则找出评分
        empty_list2.extend(mode.findall(onebookscore))
    for onebookscore in empty_list2:#吧字符串转换成整型
        score_list.append(int(onebookscore))
    return score_list

def insertToMongodb(info,name):
    info['_id'] = name
    client = MongoClient()
    db = client.test1
    collection = db.books1
    try:
        collection.save(info)
    except:
        print('保存进数据库失败')
        return False
    return True

if __name__=='__main__':
    onelist = getBooksMarking(getHtmlData(url,cookies,headers))
    insertToMongodb(onelist,'不驯的羔羊')
    print(onelist)
