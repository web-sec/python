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
for n in range(10):
    book = mycollection.find_one({'iscrawlered':0})
    url_header = 'https://book.douban.com/subject/'
    book_id = book['bookid']
    book_url = url_header + str(book_id) +'/'
    print(book_url)
