#!python3
#-*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
import time
import re
import pymongo
import random

a= {'node.js':1}
b={}
for key in a.keys():
    k2 = key.replace('.','')
    b[k2]=a[key]
print(b)
