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
    tags=[]
    myclient = mongodb.getClient()
    mycollection = myclient['doubanbooks']['tags']
    uncrawleredtag = mycollection.find({'iscrawlered':0},{'tagname':1})
    for tag in uncrawleredtag:
        tags.append(tag['tagname'])
    myclient.close()
    return tags

def getBookInfo(soup):
    books={}#每本书的id和名字,形如{'西游记':123456}
    mode = re.compile(r'subject/(.+?)/')#取subject后面的数字id
    a_list = soup.select('div.info > h2 > a')
    for a in a_list:
        href = a.attrs['href']
        book_id = mode.findall(href)
        if len(book_id)>0:
            books[a.attrs['title']] = book_id[0]
        else:
            continue
    return (reader_crawler.deleteDot(books))#去掉dot

#该函数返回了一个标签下所有书的名字和id
def getOneTagBookInfoAll(tagname,startpage=0):
    index=startpage
    next_url = True
    url_header = 'https://book.douban.com/tag/'
    url_center = '?start='
    url_foot = '&type=T'
    url = url_header+str(tagname)+url_center+str(startpage*20)+url_foot
    try:
        while next_url:
            info={}
            index+=1
            print(url)
            soup = reader_crawler.getHtmlData(url,reader_crawler.cookies,reader_crawler.headers)
            one_page_info = getBookInfo(soup)
            info.update(one_page_info)
            next_url = reader_crawler.getNextUrl(soup)
            url = 'https://book.douban.com' + str(next_url)
            saveToDoubanbooks(info,index,tagname)
            print('第%s页完成！'%index)
        setTagFlag(tagname)#将爬取过的标签标记为已爬取
    except Exception as e:
        print(e)

def setTagFlag(tag):
    myclient = mongodb.getClient()
    mycollection = myclient.doubanbooks.tags
    mycollection.update_one({'bookname':tag},{'$set':{'iscrawlered':1}})
    myclient.close()

def getStartPage(tagname):
    startpage =0
    myclient = mongodb.getClient()
    mycollection = myclient.doubanbooks.tags
    tag = mycollection.find_one({'tagname':tagname})
    try:
        startpage = tag['startpage']
    except Exception as e:
        print(e)
    myclient.close()
    return startpage

def changeInfo(info,tagname):
    myinfo=[]
    if(isinstance(info,dict)):
        for x in info.keys():
            foo={}
            foo['bookname'] = str(x)
            foo['iscrawlered']=0
            foo['bookid'] = int(info[x])
            foo['tag']= str(tagname)
            foo['_id']= int(info[x])
            myinfo.append(foo)
    return myinfo

def saveToDoubanbooks(info,has_done_page_number,tagname):
    myinfo = changeInfo(info,tagname)
    myclient = mongodb.getClient()
    tagcollection = myclient['doubanbooks']['tags']
    tagcollection.update_one({'tagname':tagname},{'$set':{'startpage':has_done_page_number}})
    mycollection = myclient['doubanbooks']['bookinfo']
    try:
        mycollection.insert_many(myinfo)
    except Exception as e:
        print(e)
    myclient.close()

def main():
    tags = getUnCrawleredTags()
    for tag in tags:
        startpage = getStartPage(tag)
        getOneTagBookInfoAll(tag,startpage)

#------------------------------------------------------------------------
if __name__=='__main__':
    main()
