#!python3
#-*-coding:utf-8-*-
from pymongo import MongoClient
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import time
import re

#与数据库建立连接
def getClient(url='mongodb://localhost'):
    try:
        client = MongoClient(url)
        return client
    except Exception as e:
        print (e)
        print('连接指定集合失败！')
        return False

#断开连接
def closeClient(client):
    client.close()

#该函数接受希望保存进数据库的数据集（字典形式的）和一个name做该文档的_id。保存方式为save，意味着每次都会覆盖同意id的数据
def saveToMongodb(info,mycollection,_id):
    info.update({'_id':_id})
    try:
        mycollection.save(info)
    except Exception as e:
        print (e)
        print('保存进数据库失败')
        return False
    return True

#爬取指定id的人的歌单
def getMusicList(p_id):
    all_music_list={}
    url = 'http://music.163.com/#/user/home?id='+str(p_id)
    #使用无界面浏览器phantomjs打开页面
    driver = webdriver.PhantomJS(executable_path='/usr/local/phantomjs/bin/phantomjs')
    #使用火狐浏览器打开页面
    #driver = webdriver.Firefox()
    try:
        #设置超时时间
        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)
        driver.get(url)
        time.sleep(1)
    except:
        #超时了就停止加载
        driver.execute_script('window.stop()')
    driver.switch_to.frame(driver.find_element_by_name("contentFrame"))#很关键的一句，进入frame再模拟操作
    html = driver.page_source#没有上面那句，直接获取源码，得到的不是我们想要的
    driver.close()
    soup = BeautifulSoup(html,'lxml')
    a_list=soup.select('#cBox > li > div > a.msk')
    hrefs=[]
    for a in a_list:
        hrefs.append(a.attrs['href'])
    return hrefs

def getMusic(href):
    all_music_list={}
    url = 'http://music.163.com/#'+href
    driver = webdriver.PhantomJS(executable_path='/usr/local/phantomjs/bin/phantomjs')
    #driver = webdriver.Firefox()
    try:
        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)
        driver.get(url)
        time.sleep(1)
    except:
        driver.execute_script('window.stop()')
    driver.switch_to.frame(driver.find_element_by_name("contentFrame"))#很关键的一句，进入frame再模拟操作
    html = driver.page_source#没有上面那句，直接获取源码，得到的不是我们想要的
    driver.close()
    soup = BeautifulSoup(html,'lxml')
    b_list=soup.select('#song-list-pre-cache > div > div > table > tbody > tr > td > div > div > div > span > a > b')
    titles=[]
    for b in b_list:
         titles.append(b.get_text())
    return titles

#从数据库拿未爬过的人的信息
def getAllPeopleInfoFromDB():
    name_id = {}
    myclient = getClient()
    mycollection = myclient['music']['peopleinfo']
    cursor = mycollection.find({'iscrawlered':0})
    for x in cursor:
        name_id.update({x['name']:x['id']})
    myclient.close()
    return name_id

#爬过以后给这个id的爬取标签设为1
def makeCrawleredFlag(id):
    myclient = getClient()
    mycollection = myclient['music']['peopleinfo']
    mycollection.update_one({'id':str(id)},{'$set':{'iscrawlered':1}})
    myclient.close()

def test(name,id):
    myclient = getClient()
    mydb = myclient['music']
    mycollection = mydb[name]
    music_list = getMusicList(id)
    all_musics = []
    for href in music_list:
        music = getMusic(href)
        all_musics=list(set(all_musics+music))
    saveToMongodb({'music':all_musics},mycollection,id)
    makeCrawleredFlag(id)
    print(name)
    print(all_musics)
    closeClient(myclient)

if __name__ == '__main__':
    #test('午饭','257572397')

    myclient = getClient()
    mydb = myclient['music']

    peoples_info = getAllPeopleInfoFromDB()
    people_len = len(peoples_info)
    print('还要爬' + str(people_len) + '个人!')
    m=0
    for name,id in peoples_info.items():
        m+=1
        print(name+ ' 一共 '+ str(people_len) + ' 个，当前第' + str(m) + ' 个！' )
        mycollection = mydb[name]
        music_list = getMusicList(id)
        music_list_len = len(music_list)
        all_musics = []
        n=0
        for href in music_list:
            n+=1
            music = getMusic(href)
            print(' 此人有 '+ str(music_list_len) + ' 个歌单,当前完成第' + str(n) + '个')
            all_musics=list(set(all_musics+music))
        saveToMongodb({'music':all_musics},mycollection,id)
        makeCrawleredFlag(id)
        print(name +'已完成！')
