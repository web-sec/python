#!python3
#-*-coding:utf-8-*-
from bs4 import BeautifulSoup
import re
from pymongo import MongoClient
import mongodb
import reader_crawler
#获取豆瓣读书的所有书类型
url_header = 'https://book.douban.com/tag/'
def getUnCrawleredTags():
    tags = []
    try:
        myclient = mongodb.getClient()
        tags_cursor = mongodb.getDBInfo(myclient,'doubanbooks','tags')
        for document in tags_cursor:
            if isinstance(document['bookname'],str) and document['iscrawlered']==0:
                tags.append(document['bookname'])
        myclient.close()
    except Exception as e:
        print(e)
    return tags

def getBookInfo(soup):
    books={}#每本书的id和名字
    mode = re.compile(r'subject/(.+?)/')#取subject后面的数字id
    a_list = soup.select('div.info > h2 > a')
    try:
        for a in a_list:
            href = a.attrs['href']
            books[a.attrs['title']] = mode.findall(href)[0]
    except Exception as e:
        print (e)
    return (reader_crawler.deleteDot(books))#去掉dot

def getBookInfoAll():
    info={}
    tags = getUnCrawleredTags()
    for tag in tags:
        index=0
        next_url = True
        url = url_header+str(tagname)

        while next_url:
            index+=1
            soup = reader_crawler.getHtmlData(url,reader_crawler.cookies,reader_crawler.headers)
            one_page_info = getBookInfo(soup)
            info.update(one_page_info)
            next_url = reader_crawler.getNextUrl(soup)
            url = 'https://book.douban.com' + str(next_url)
            print('第%s页完成！'%index)

        setTagFlag(tag)#将爬取过的标签标记为已爬取
    return info#返回某标签中所有的书的信息

def setTagFlag(tag):
    myclient = mongodb.getClient()
    mycollection = myclient.doubanbooks.tags
    mycollection.update_one({'bookname':tag},{'$set':{'iscrawlered':1}})
    myclient.close()

#------------------------------------------------------------------------
if __name__=='__main__':
    tags = getAllTags();
