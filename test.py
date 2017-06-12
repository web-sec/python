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
import reader_crawler

tags=[]
myclient = mongodb.getClient()
tags_cursor = mongodb.getDBInfo(myclient,'doubanbooks','tags')
for document in tags_cursor:
    if isinstance(document['bookname'],str) and document['iscrawlered']==0:
        tags.append(document['bookname'])
myclient.close()
print(tags)
