#!python3
#-*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
import time
import re
import pymongo
import random
import urllib.request
import http.cookiejar
from pymongo import MongoClient

#url="https://book.douban.com/people/john91/collect"
#获取指定的url页面的信息，返回的是bs4.BeautifulSoup对象
# def makeMyOpener(head = {
#     'Connection': 'Keep-Alive',
#     'Accept': 'text/html, application/xhtml+xml, */*',
#     'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
# }):
#     cj = http.cookiejar.CookieJar()
#     opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
#     header = []
#     for key, value in head.items():
#         elem = (key, value)
#         header.append(elem)
#     opener.addheaders = header
#     return opener
#
# oper = makeMyOpener()
# res = oper.open(url)
# data = res.read()
url = "http://bbs.fishc.com/thread-61960-1-1.html"
head = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
req = urllib.request.Request(url,None,head)
res = urllib.request.urlopen(req)
print(res)
data = res.read()
html = data.decode('gbk','ignore')
soup = BeautifulSoup(html, "lxml")
a = soup.select('div > a')

info = {}
n=0
for x in a:
    n+=1
    s = str(n)
    text = x.get_text()
    info[s]=text

client = MongoClient()
db = client.test1.books1
result=db.insert_one(info,'_id':"www")
