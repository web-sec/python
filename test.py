#!python3
#-*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
import time
import re
import pymongo
import random
import urllib.request

url="ct/1012611/collections"
if type(url)=='string':
    print("ok")
else:
    print(type(url))
