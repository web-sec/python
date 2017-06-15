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

a = datetime.datetime.now()
reader_crawler.getSleep(3,4)
b = datetime.datetime.now()
t = b-a
print('d'+str(t))
