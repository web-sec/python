#!python3
#-*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
import time
import re
import pymongo
import random
import reader_crawler
import mongodb

c = mongodb.getClient()
g =c.doubanbooks.tags

f=g.find({'tagname':'自助游'},{'tagname':1,'startpage':1})
for x in f:
    print(x)
