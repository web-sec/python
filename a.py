#!python3
#-*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
import time
import re
import os
import pymongo
import random
import urllib.request
import urllib.parse
import http.cookiejar
from pymongo import MongoClient

url = "http://www.douban.com"
r = requests.get(url)
h = r.request.headers['User-Agent']
print(h)
headers = {'User-Agent':h}
