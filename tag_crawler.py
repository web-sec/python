#!python3
#-*-coding:utf-8-*-
from bs4 import BeautifulSoup
import re
from pymongo import MongoClient
import mongodb
import reader_crawler
#获取豆瓣读书的所有书类型
url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'
soup = reader_crawler.getHtmlData(url,reader_crawler.cookies,reader_crawler.headers)
a_list = soup.select('table.tagCol > tbody > tr > td > a')
mode =re.compile(r'.*?\((\d+?)\)')
for a in a_list:
    tag_dict = {}
    name = a.get_text()#tag名
    tag_dict.update({'tagname':name,'iscrawlered':0,'startpage':0})#该标签未爬取过，设为0，爬取过了，设为1
    myclient = mongodb.getClient()
    mydb = myclient.doubanbooks
    try:
        mycollection = mydb.tags
        mongodb.saveToMongodb(tag_dict,mycollection)#保存进数据库
    except Exception as e:
        print(e)
