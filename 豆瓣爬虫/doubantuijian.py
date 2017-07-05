#!python3
#-*-coding:utf-8-*-
import distance
import mongodb

def changeDict(dictionary):
    newdict = {}
    doc_id = dictionary['_id']
    del dictionary['_id']
    del dictionary['id']
    newdict[doc_id] = dictionary
    return newdict

#获取指定集合里的指定数量的数据，然后格式化后输出
def getRightData(db_name,collection_name,document_number):
    index = 0
    mydict = {}
    myclient = mongodb.getClient()
    if isinstance(db_name,str)&&isinstance(collection_name,str):
        try:
            cursor = mongodb.getDBInfo(myclient,db_name,collection_name)
        except Exception as e:
            print (e)
    #逐条获取数据库里的数据，然后格式化成我们需要的形式，如{'人名':{'书名':评分,...}}
    for document in cursor:
        if index<document_number:
            index+=1
            d = changeDict(document)
            for key in d.keys():
                mydict[key] = d[key]
        else:
            break
    myclient.close()
    return mydict
#----------------------------------------------
if __name__=='__main__':
    mydict = getRightData('test1','books2',10)
    mydict['wufan']={'Nodejs实战':4,'嫌疑人X的献身':4,'鲁滨逊漂流记': 4,'三体': 5, '三体Ⅱ': 4, '三体Ⅲ': 3,'jQuery实战（第2版）': 5}
    itemsim=distance.calculateSimilarItems(mydict)
    print(distance.getRecommendedItems(mydict,itemsim,'wufan'))
