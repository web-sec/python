#!python3
#-*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
import time
import re
import pymongo
import random

a=['a','b','c']
b=[1,2,3]
c={}
for x in range(0,len(a)):
    c[a[x]]=b[x]
print(c)
