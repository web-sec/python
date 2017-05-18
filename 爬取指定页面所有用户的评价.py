#!python3
#-*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
import time
import re
import pymongo
import random
import urllib.request

url="https://book.douban.com/people/john91/collect"
#获取指定的url页面的信息，返回的是bs4.BeautifulSoup对象
def getHtmlData(url):
    try:
        res = urllib.request.urlopen(url)
        html = res.read()
        data = html.decode("utf-8")
        soup = BeautifulSoup(data, "lxml")
    except:
        print("can't getHtmlData!")
    else:
        return soup

if __name__ == '__main__':
    html = getHtmlData(url)
    books_divs = html.find_all('div',attrs={"class":"pub"})
    print(len(books_divs))
    books = []
    for book in books_divs:
        try:
            books.append(books_divs.get_text())
        except:
            pass
