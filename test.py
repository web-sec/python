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

cookies = {'cookie':'ll="118159"; bid=rIFKNErGPjM; viewed="2042063"; gr_user_id=6302343c-4d52-4903-86d3-72e66cd99228; ps=y; ue="495464616@qq.com"; __ads_session=ggwUaKo46gjw+v8AIAA=; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=6521c349-5966-4355-847a-a67548809e6a; gr_cs1_6521c349-5966-4355-847a-a67548809e6a=user_id%3A1; __utmt_douban=1; __utma=30149280.886896177.1484292481.1495594251.1495676585.6; __utmb=30149280.1.10.1495676585; __utmc=30149280; __utmz=30149280.1495676585.6.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _vwo_uuid_v2=B5D7C7975C5D7F6241ADD9533A376ABA|50e0f527e7cb50ccd1ec80fde50abfcf; push_noty_num=0; push_doumail_num=0; ap=1; as="https://book.douban.com/"'}
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
url = 'https://book.douban.com/subject/1012611/collections'
def getHtmlData(url,cookies,headers):
    try:
        r = requests.get(url,cookies=cookies,headers=headers)
        r.encoding = 'utf-8'
        content = r.text
        soup = BeautifulSoup(content,'lxml')
    except:
        print('get '+url+' failed!')
    return soup

a = getHtmlData(url,cookies,headers)
print(a)
