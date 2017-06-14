#!python3
#-*-coding:utf-8-*-
# import requests
# from bs4 import BeautifulSoup
import time
import re
import pymongo
import random
from pymongo import MongoClient
import math
import mongodb
# import reader_crawler

myclient = mongodb.getClient()
mycollection = myclient['doubanbooks']['bookinfo']
mycollection.update_one({'bookname':'出国自助游教室'},{'$set':{'iscrawlered':1}})
a=mycollection.find_one({'bookname':'出国自助游教室'})
print(a['iscrawlered'])
myclient.close()
