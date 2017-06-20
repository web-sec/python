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
import datetime
import reader_crawler

class Mongo(object):
    """docstring for Mongodb."""
    def __init__(self,db_name,collection_name):
        self.url = 'mongodb://localhost'
        self.db_name = db_name
        self.collection_name = collection_name
        self.username = ''
        self.password = ''
        self.client = MongoClient(self.url)[self.db_name][self.collection_name]


    def close(self):
        self.client.close()

    def findOne(self,attrs):
        return self.client.find_one(attrs)

m = Mongo('doubanbooks','tags')
print(m.findOne({'tagname':'小说'}))
