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

def getSleep(timemin,timemax):
    time.sleep(round(random.uniform(timemin,timemax),2))
    stdout.flush()

for x in range(1,4):
    print('1')
    getSleep(1,2)
