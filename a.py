#!python3
#-*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
import time
import re
import pymongo
import random

a=[1,2,3,4]
b=[5,6,7,8]
for x,y in zip(a,b):
    p = {x:y}
    print(p)
