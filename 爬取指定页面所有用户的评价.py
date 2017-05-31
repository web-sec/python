#!python3
#-*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
import time
import re
import math
import pymongo
import random
from pymongo import MongoClient
from sys import stdout


url_book = 'https://book.douban.com/subject/1007305/collections'
#第二页开始的url形式为https://book.douban.com/people/john91/collect?start=15&sort=time&rating=all&filter=all&mode=grid
url_1 = "?start="
url_2 = "&sort=time&rating=all&filter=all&mode=grid"
cookies = {'cookie':'ll="118159"; bid=rIFKNErGPjM; viewed="2042063"; gr_user_id=6302343c-4d52-4903-86d3-72e66cd99228; ps=y; ue="495464616@qq.com"; __ads_session=ggwUaKo46gjw+v8AIAA=; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=6521c349-5966-4355-847a-a67548809e6a; gr_cs1_6521c349-5966-4355-847a-a67548809e6a=user_id%3A1; __utmt_douban=1; __utma=30149280.886896177.1484292481.1495594251.1495676585.6; __utmb=30149280.1.10.1495676585; __utmc=30149280; __utmz=30149280.1495676585.6.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _vwo_uuid_v2=B5D7C7975C5D7F6241ADD9533A376ABA|50e0f527e7cb50ccd1ec80fde50abfcf; push_noty_num=0; push_doumail_num=0; ap=1; as="https://book.douban.com/"'}
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

#该函数依据传入的url地址，使用chrome浏览器的header，豆瓣读书登入后的cookie，utf-8解码，返回该页面的一个BeautifulSoup对象
def getHtmlData(url,cookies,headers):
    try:
        getSleep(3,4)
        r = requests.get(url,cookies=cookies,headers=headers)
        r.encoding = 'utf-8'
        content = r.text
        soup = BeautifulSoup(content,'lxml')
        return soup
    except:
        print('get '+url+' failed!')
        return False

#该该函数返回看过某本书的用户的列表，可选定爬取的数量
def getPeopleList(soup,length):
    peoples = []
    peoples_href = soup.select('div.pl2 > a')

#该函数返回指定用户已阅读书本数量，返回值为int型
def getBookQuantity(soup):
    mode =re.compile(r'.+?\((\d+?)\)')
    h1 = soup.select('#db-usr-profile > .info > h1')
    h1_text = h1[0].get_text()
    book_quantity = int(mode.findall(h1_text)[0])
    return book_quantity

#该函数返回指定页面每本书的评价，返回一个{‘书名’：评价分}的字典
def getBooksMarking(soup,pages=-1):
    booknames = []
    bookscores = []
    evaluatioin = {}
    booklist_a = soup.select('.article > ul > li > .info > h2 > a')
    booklist_span = soup.select('.article > ul > li > .info > .short-note > div > span:nth-of-type(1)')
    for book in booklist_a:
        booknames.append(book.attrs['title'])#booknames列表存储了当前页面所有书的名字，形式为['乌合之众', '菊与刀', '孟子趣说3', '孟子趣说2', '孟子趣说1', '逍遥游', '我们为什么离正义越来越远', '中国思想地图', '《理想国》讲演录', '春秋大义', '理想国', '且介亭杂文末编', '且介亭杂文二集', '现象学导论', '且介亭杂文']
    for book in booklist_span:
        bookscores.append(book.attrs['class'])#bookscores列表存储了当前页面书本的评分，形式为[['rating4-t'], ['rating4-t'], ['rating4-t'], ['rating4-t'], ['rating4-t'], ['rating4-t'], ['rating5-t'], ['rating4-t'], ['rating4-t'], ['rating4-t'], ['rating5-t'], ['rating4-t'], ['rating4-t'], ['rating4-t'], ['rating4-t']]
    score_list = getBookScores(bookscores)
    if len(booknames) != len(score_list):#书本名数量和书本评价数量不符时
        print('第'+str(pages)+'页书名与评价数量不符！')
        return False
    else:#数量一致时
        for index in range(0,len(booknames)):
            if score_list[index]!=-1:
                evaluatioin[booknames[index]]=score_list[index]
            else:
                continue
        return evaluatioin

#该函数处理一下爬取到的书本评价分，以列表形式返回每本书的评价分，元素为int型
def getBookScores(scorelist):
    empty_list1 = []
    empty_list2 = []
    score_list = []
    mode = re.compile(r'\d+')
    for onebookscore in scorelist:#去除中括号
        empty_list1.append(onebookscore[0])
    for onebookscore in empty_list1:#正则找出评分
        a_list = mode.findall(onebookscore)
        if len(a_list)==0:
            a_list.append(-1)
        empty_list2.extend(a_list)
    for onebookscore in empty_list2:#吧字符串转换成整型
        score_list.append(int(onebookscore))
    return score_list

#该函数返回一个字典，其中包含了一个读者的所有看过的书和该书的评价
def getAllBookScores(url,soup):
    url_1 = "?start="
    url_2 = "&sort=time&rating=all&filter=all&mode=grid"
    all_book_scores = {}
    book_quantity = getBookQuantity(soup)#获得已看书本的总数
    for pages in range(0,math.ceil(book_quantity/15)):#每15本书一页
        one_page_url = url + url_1 + str(pages*15) +url_2
        one_page_soup = getHtmlData(one_page_url,cookies,headers)
        one_page_scores = getBooksMarking(one_page_soup,pages+1)
        all_book_scores = dict(all_book_scores,**one_page_scores)
        print('总共 '+str(math.ceil(book_quantity/15))+' 页,第 '+str(pages+1)+' 页已爬完！')
    return all_book_scores

#该函数接受希望保存进数据库的数据集（字典形式的）和一个name做该文档的_id。保存方式为save，意味着每次都会覆盖同意id的数据
def saveToMongodb(info,name):
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

#该函数实现在规定范围内随机一段休眠时间，防止爬取过快被封ip
def getSleep(timemin,timemax):
    time.sleep(round(random.uniform(timemin,timemax),2))
    stdout.flush()#此方法用于实时print数据

#该函数返回当前页面(特指一本书的已看过人的页面)的下个页面的url
def getNextUrl(soup):
    try:
        next_url = soup.select_one('span.next > a').attrs['href']
        if isinstance(next_url,str):
            return next_url
    except:
        return False

#该函数爬取了一个页面中所有的含有用户名字的href获取其id，以及用户名，返回两个队列，第一个是id,第二个是用户名
def getOnePagePeople(soup):
    ids = []
    names = []
    next_url = getNextUrl(soup)
    people_id = soup.select('div.pl2 > a')
    people_name = soup.select('div.pl2 > a > span:nth-of-type(1)')
    for x in people_id:
        ids.append(getPeopleId(x.attrs['href']))
    for y in people_name:
        names.append(y.get_text())
    if len(people_id)==len(people_name):
        return ids,names
    else:
        return False
#该函数获取指定页数的用户id和用户名,每页包含20人
def getAllPeople(url,page_quantity):
    all_peoples = []
    all_name = []
    for page in range(0,math.ceil(page_quantity)):
        if url:
            soup = getHtmlData(url,cookies,headers)
            peoples_tuple = getOnePagePeople(soup)
            if peoples_tuple:
                ids = peoples_tuple[0]
                names = peoples_tuple[1]
            else:
                ids = []
                names = []
            all_peoples += ids
            all_name += names
            url = getNextUrl(soup)
            print('总计 '+str(math.ceil(page_quantity))+' 页,已完成 '+str(page+1)+' 页')
        else:
            break
    return all_peoples,all_name

#获取形如'https://www.douban.com/people/46397373/'的字符串中的数字id
def getPeopleId(people_id_url):
    mode = re.compile(r'people/(.+?)/')
    people_id = mode.findall(people_id_url)
    if len(people_id)>0:
        return people_id[0]
    else:
        print('获取 '+people_id_url+' 的id失败！')
        return False

def getAllPeopleBookScores(url,page_quantity):
    total_info=0
    index = 0
    url_header = 'https://book.douban.com/people/'
    url_foot = '/collect'
    peoples = getAllPeople(url,page_quantity)
    peoples_id = peoples[0]#用户id数组
    peoples_name = peoples[1]#用户名字数组
    for p_id,p_name in zip(peoples_id,peoples_name):
        index+=1
        people_collect_url = url_header+p_id+url_foot
        soup = getHtmlData(people_collect_url,cookies,headers)
        print('本次任务打算爬取 '+str(len(peoples_id))+' 名用户，当前是第 '+str(index)+' 名,url是 '+people_collect_url)
        all_book_scores = getAllBookScores(people_collect_url,soup)
        total_info+=len(all_book_scores)
        print(p_name+' 总共看过 '+str(getBookQuantity(soup))+' 本书,其中已获取有效数据 '+str(len(all_book_scores))+' 条')
        issaved = saveToMongodb(all_book_scores,p_name)
        if issaved:
            print(p_name+" 的数据已保存！")
    print('本次爬取结束，总共获得 '+total_info+' 条有效数据！')
#-------------------------------分割线----------------------------
if __name__=='__main__':
    getAllPeopleBookScores(url_book,20)
