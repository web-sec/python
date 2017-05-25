#!python3
#-*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
import time
import re
import pymongo
import random
from pymongo import MongoClient

n=0
b={}
client = MongoClient()
db = client.test1
collection = db.books1
a =['乌合之众', '菊与刀', '孟子趣说3', '孟子趣说2', '孟子趣说1', '逍遥游', '我们为什么离正义越来越远', '中国思想地图', '《理想国》讲演录', '春秋大义', '理想国', '且介亭杂文末编', '且介亭杂文二集', '现象学导论', '且介亭杂文']
for x in a:
    n+=1
    b[x] = n
b['_id']="1"

collection.save(b)
