#!python3
#-*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
import time
import re
import pymongo
import random

mode = re.compile(r'\d+')
a = mode.findall('data')
print(a)
