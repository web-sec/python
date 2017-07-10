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

class Fruit:
    price = 0
    def __init__(self):
        self.__color = 'red'

    def getColor(self):
        print(self.__color)

    def changePrice(self):
        Fruit.price += 10

    def r(self):
        return Fruit.getColor(self)
if __name__ == '__main__':
    apple = Fruit()
    apple.r()
