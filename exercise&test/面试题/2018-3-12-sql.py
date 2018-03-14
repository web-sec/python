#*-coding:utf-8-*
import sqlite3
def ConnectToDB(dbname='test.db'):
    conn = sqlite3.connect(dbname)
    return conn

def ExecuteDB(content,dbname='test.db'):
    conn = ConnectToDB(dbname)
    c = conn.cursor()
    c.execute(content)
    conn.commit()
    conn.close()
    return

def SelectDB(content,dbname='test.db'):
    conn = ConnectToDB(dbname)
    c = conn.cursor()
    p = c.execute(content)
    for i in p:
        print(i)
    conn.close()
    return

def InsertIntoB():
    ids = [1,2,3,4,5]
    names = ['高数','线代','算法','历史','语文']
    insert_table_B = ''
    for cid,cname in zip(ids,names):
        insert_table_B = "insert into B(CID,CNAME) values ({cid},'{cname}');".format(cid=cid,cname=cname)
        print(insert_table_B)
        ExecuteDB(insert_table_B)
    return

def InsertIntoC():
    cids = [1,1,2,2,2,4,5]
    sids = [101,102,101,103,104,101,103]
    scores = [10,10,10,10,10,10,10]
    insert_table_B = ''
    for cid,sid,score in zip(cids,sids,scores):
        insert_table_C = "insert into C(CID,SID,SCORE) values ({cid},{sid},{score});".format(cid=cid,sid=sid,score=score)
        print(insert_table_C)
        ExecuteDB(insert_table_C)
    return
#create_table_B = "create table B (CID int(16) primary key not null,CNAME char(256));"
#create_table_C='create table C (SID int not null,CID int not null,SCORE float(3,1),primary key(SID,CID));'
# SelectDB('select * from A')

#SelectDB('select SNAME from A where not exists(select distinct SID from C where CID=5)')
#SelectDB('select SNAME from A where SID !=(select distinct SID from C where CID=5)')


SelectDB('select * from C')
print('----------------')
ExecuteDB('delete from C where CID=4')
SelectDB('select * from C')
