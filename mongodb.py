#!python3
#-*-coding:utf-8-*-
from pymongo import MongoClient


#与数据库建立连接
def getClient(url='mongodb://localhost'):
    try:
        client = MongoClient(url)
        return client
    except:
        print('连接指定集合失败！')
        return False

#断开连接
def closeClient(client):
    client.close()

#该函数接受希望保存进数据库的数据集（字典形式的）和一个name做该文档的_id。保存方式为save，意味着每次都会覆盖同意id的数据
def saveToMongodb(info,client,dbname,collection_name):
    db=client[dbname]#数据库名
    collection=db[collection_name]#集合名
    try:
        collection.save(info)
    except:
        print('保存进数据库失败')
        return False
    return True

#该函数返回指定数据库、集合的所有文档的游标
def getBDInfo(db,collection_name):
    myclient = getClient()
    mydb = myclient[db]
    mycollection = mydb[collection_name]
    cursor = mycollection.find()
    return cursor
if __name__=='__main__':
    c = getBDInfo('test1','books3')
    for x in range(0,3):
        if c[x]:
            print(c[x])
