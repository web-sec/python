#!python3
#-*-coding:utf-8-*-
from pymongo import MongoClient
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import time
import re


def getNameAndId(soup):
    a_list = soup.select('#main-box > li > a')
    p = {}
    mode = re.compile(r'id=(\d+)')
    for a in a_list:
        name = a.attrs['title']
        p_id = mode.findall(a.attrs['href'])[0]
        p[name] = p_id
    return p

#爬取所有关注人的用户名和id
def getAllPeopleInfo(url):
    all_peoples_info={}
    #driver = webdriver.PhantomJS(executable_path='/usr/local/phantomjs/bin/phantomjs')
    driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(1)
    driver.switch_to.frame(driver.find_element_by_name("contentFrame"))#很关键的一句，进入frame再模拟操作
    while True:
        print('once')
        html = driver.page_source#获取源代码
        soup = BeautifulSoup(html,'lxml')
        p = getNameAndId(soup)
        all_peoples_info.update(p)
        driver.execute_script("var q=document.documentElement.scrollTop=5000")#拉到页面底部
        time.sleep(1)
        button = driver.find_element_by_class_name("znxt")
        class_list = button.get_attribute('class').split()
        if class_list[-1] == 'js-disabled':
            break
        ActionChains(driver).click(button).perform()
        time.sleep(1)
    driver.close()
    return all_peoples_info

if __name__ == '__main__':
    url= 'http://music.163.com/user/follows?id=67862260'
    all_peoples_info = getAllPeopleInfo(url)
    myclient = MongoClient('mongodb://localhost')
    mycollection = myclient['music']['peopleinfo']
    for name,id in all_peoples_info.items():
        info = {'_id':id,'name':name,'id':id,'iscrawlered':0}
        mycollection.save(info)
    myclient.close()
