#!python3
#-*-coding:utf-8-*-
from pymongo import MongoClient
book=[]
client=MongoClient()
db=client.test1
collection=db.books1
books=collection.find({"_id":"mybooks"})
for x in books:
    book.append({x,books[x]})
print(book)
#if __name__=='__main__':
