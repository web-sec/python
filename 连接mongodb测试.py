#!python3
#-*-coding:utf-8-*-
from pymongo import MongoClient
book=[]
client=MongoClient()
db=client.test1
collection=db.books1
books=collection.find_one({"_id":"mybooks"})
if '_id' in books:
    del(books['_id'])
for key in books:
    print(books[key])
#if __name__=='__main__':
