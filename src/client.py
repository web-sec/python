#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from io import BytesIO
import configparser
import hashlib
import os
import pycurl
import threading
import time
#import re
#import tempfile
import zipfile
#import zmq
#import urllib.request
import Hxdetect
url = ''
fileU = None

def getConfigInfo():#获取配置文件信息
    config = configparser.ConfigParser()#初始化实例
    config_file = 'config/Client.conf'#配置文件放在当前目录下
    config.read(config_file)#读取配置信息
    scanners = {}#=>{'ClamAV':'localhost',...}
    for scanner in config.sections():#获取所有sections。也就是将配置文件中所有“[ ]”读取到列表中
        if scanner != 'Local':
            scanners[scanner] = config[scanner]['IP']
    global url
    url = config['URL']['IP']
    return scanners
#获取指定文件夹下所有文件的路径，返回列表
def getFilePath(dirpath):#参数是相对路径
    all_file_path=[]
    for root,dirs,files in os.walk(dirpath):
        for file in files:
            all_file_path.append(os.path.join(root,file))
    return all_file_path
#上传指定文件到指定ip
def upload(url,filepath):
    storage = BytesIO()
    # false=bool(False)
    field = "archive"
    c = pycurl.Curl()
    c.setopt(c.POST, 1)
    c.setopt(c.URL,url)
    c.setopt(c.WRITEFUNCTION,storage.write)
    c.setopt(c.HTTPPOST, [(field,(c.FORM_FILE,filepath))])
    c.perform()
    c.close()
    
    content = storage.getvalue()
    content=content.decode('utf-8')
    dictinfo=eval(content)
    return dictinfo['md5']

def getCloudResult():
    storage = BytesIO()
    dictinfo = ''
    try:
        d = pycurl.Curl()
        d.setopt(d.URL,"http://"+url+"/"+fileU)
        d.setopt(d.WRITEFUNCTION,storage.write)
        d.perform()
        d.close()
        content = storage.getvalue()
        content=content.decode('utf-8')
        dictinfo=eval(content)
    except: 
        print ''
    return dictinfo

#将指定字符串进行md5加密
def md5(s):
    if type(s) == (bytes or str):
        m = hashlib.md5()
        m.update(s)
        return m.hexdigest()
    else:
        return ''

def action(arg):
    doIt(arg)

def doInCloud(i):
    t =threading.Thread(target=action,args=(i,))
    t.start()


def actionG(arg):
    dic = {'file':'none'}
    while fileU is None:
        time.sleep(0.2)
    
    dic = getCloudResult()
    cnt = 0
    while dic['file'] is 'none' and cnt < 10:
        time.sleep(2)
        cnt +=1
        dic = getCloudResult()
    
    if dic['file'] is 'none':
         print 'Cloud Scaned End!!Connetion is over 10'
         return

    if dic['file'] is not 'none':
        for key, value in dic['fileList'].items():
            exist = False
            for res in Hxdetect.ShellDetector._resList:
                if key in res[0]:
                    exist = True
                    break
            if exist is False:
                Hxdetect.ShellDetector._resList.append([key,value])
                Hxdetect.ShellDetector._filesCount += 1
                Hxdetect.ShellDetector._badfiles.append(key)
                print key +":" +value
    Hxdetect.ShellDetector.alert('Cloud Scaned Status: ' + str(Hxdetect.ShellDetector._filesCount) + ' suspicious files and ' + str(len(Hxdetect.ShellDetector._badfiles)) + ' shells', 'red')    
    
    lenZnt = 0
    leng = len(dic['fileList'])
    lengCnt = 0
    while True:
        dic = getCloudResult()
        if dic['file'] is not 'none':
            for key, value in dic['fileList'].items():
                exist = False
                for res in Hxdetect.ShellDetector._resList:
                    if key in res[0]:
                        exist = True
                        break
                if exist is False:
                    Hxdetect.ShellDetector._resList.append([key,value])
                    Hxdetect.ShellDetector._filesCount += 1
                    Hxdetect.ShellDetector._badfiles.append(key)
                    print key +":" +value
        if len(Hxdetect.ShellDetector._badfiles)!=lenZnt:
            lenZnt = len(Hxdetect.ShellDetector._badfiles)
            Hxdetect.ShellDetector.alert('Cloud Scaned Status: ' + str(Hxdetect.ShellDetector._filesCount) + ' suspicious files and ' + str(len(Hxdetect.ShellDetector._badfiles)) + ' shells', 'red')    
        if leng == len(dic['fileList']):
            lengCnt += 1
        else:
            lengCnt = 0
        if lengCnt > 3:
            print 'Cloud Scaned End'
            break
        leng = len(dic['fileList'])
        time.sleep(5)

def doGetCloud(i):
    t =threading.Thread(target=actionG,args=(i,))
    t.start()
    
#将指定的单个文件压缩，压缩包名字为文件名的md5加密，解压后文件名不变,压缩包位置自定义
def zip_file(path,zipfilepath=''):
    
    zipfilename = md5(str(time.localtime()))+'.zip'
    zf = zipfile.ZipFile(os.path.join(zipfilepath,zipfilename), "w", zipfile.ZIP_STORED,allowZip64=True)
    
    for root, dirs, files in os.walk(path):
        for filename in files:
            filepath = os.path.join(root, filename)
#            file = os.path.basename(filepath)
            zf.write(filepath,filepath)

    return os.path.join(zipfilepath,zipfilename)

#def send_to_scanner(scanner, ip, filename):#参数分别为：扫描器名字，主机ip，扫描文件名
#    config_info = getConfigInfo()
#    port = config_info['port']#端口号
#    message = 'SCAN:{}:{}'.format(scanner, filename)
#    context = zmq.Context()
#    socket = context.socket(zmq.REQ)
#    socket.connect('tcp://{}:{}'.format(ip, 5555))
#    socket.send_string(message)
#    reply = socket.recv_json()
#    return reply

def doIt(dirname):
    global fileU
    config_info = getConfigInfo()
    zipfile = zip_file(dirname)#压缩文件
    fileU = upload(url,zipfile)#上传文件
#    send_to_scanner('clamav',"127.0.0.1",zipfile)
    os.remove(zipfile)#删除压缩文件
    #print('删除了'+zipfile)
    return True
