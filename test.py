#!python3
#-*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
import time
import re
import pymongo
import random
import urllib.request
import urllib.parse
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
def getHtmlData(url,values,head):
    data = urllib.parse.urlencode(values).encode(encoding='utf_8')
    req = urllib.request.Request(url,data,head)
    res = urllib.request.urlopen(req)
    data = res.read()
    html = data.decode('utf-8','ignore')
    soup = BeautifulSoup(html, "lxml")
    return soup

url1 = "https://book.douban.com/people/john91/collect"
url2 = 'https://book.douban.com'
head = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
values = {"ll":"118159",
        "bid":"rIFKNErGPjM",
         "viewed":"2042063",
         "gr_user_id":"6302343c-4d52-4903-86d3-72e66cd99228",
         "_vwo_uuid_v2":"B5D7C7975C5D7F6241ADD9533A376ABA|50e0f527e7cb50ccd1ec80fde50abfcf",
         "gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03":"4843163f-81a0-4311-a4cd-bb9b956c28e3",
         "gr_cs1_4843163f-81a0-4311-a4cd-bb9b956c28e3":"user_id%3A0",
         "__utmt_douban":"1",
         "__utma":"30149280.886896177.1484292481.1495099948.1495594251.5",
         "__utmb":"30149280.1.10.1495594251",
         "__utmc":"30149280",
         "as":"https://book.douban.com/",
         "ps":"y"}

try:
    soup = getHtmlData(url1,values,head)
except urllib.request.HTTPError as e:
    print(e.code)
except urllib.request.URLError as e:
    print(e.reason)

def getHtmlData(url,values,head):
    res = urllib.request.urlopen(req)
    data = res.read()
    html = data.decode('utf-8','ignore')
    soup = BeautifulSoup(html, "lxml")
    return soup

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
result=db.insert_one(info)
try:
    print(result.inserted_id)
except:
    print('insert failed')
