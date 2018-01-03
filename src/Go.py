#!/usr/bin/env python
import Hxdetect
import client
import datetime
import hashlib
import optparse
import os
import re
import sys
import threading
import time

absPath = ''
clear = None
record = ''
_tot = 0
_TT = 0
ISOTIMEFORMAT='%Y-%m-%d %X'

scan_extensions = []
whitelist_dir = []



def SHA1FileWithName(fineName, block_size=64 * 1024):
    with open(fineName, 'rb') as f:
        sha1 = hashlib.md5()
        while True:
            data = f.read(block_size)
            if not data:
                break
            sha1.update(data)
        retsha1 = sha1.hexdigest()
        f.close()
        return retsha1
    
def GetValue(path,fullAndFirstFlag,logFlag):
    global record
    global _TT
    fl = os.listdir(path)
    for f in fl:
        if '$' in os.path.join(path,f):
            continue
        if os.path.isdir(os.path.join(path,f)):
            GetValue(os.path.join(path,f),fullAndFirstFlag,logFlag)
        else:
            #if fullAndFirstFlag:
            _TT +=1
#            fb = open(absPath+"//config//scan_extensions")
#            fw = open(absPath+"//config//whitelist_dir")
            text = os.path.join(path,f)
            flag = False
            for line in whitelist_dir:
                line=line.strip('\n')
                if re.match(line, text, re.IGNORECASE):
#                    fb.close()
#                    fw.close()
                    flag = True
                    break
            if flag == True:
                continue
            for linez in scan_extensions:
                linez=linez.strip('\n')
                if re.search('.'+linez, text, re.IGNORECASE):
                    correctFile = True
                    sha = ''
                    if fullAndFirstFlag == True:
                        correctFile = Detect(os.path.join(path,f))
                    sha = str(SHA1FileWithName(text))
                    if correctFile == True:    
                        record += "%s+%s\n" % (text,sha)
                    else:
                        if logFlag and fullAndFirstFlag is not True:
                            Log(os.path.join(path,f),sha)
                    break
#            fb.close()
#            fw.close()
            
            
def init(options):
    fb = ''
    fw = ''
    try:
        fb = open(absPath+"//config//scan_extensions")
        for line in fb:
            line=line.strip('\n')
            scan_extensions.append(line)
        
        fw = open(absPath+"//config//whitelist_dir")
        for line in fw:
            line=line.strip('\n')
            whitelist_dir.append(line)
    finally:
        fb.close()
        fw.close()
        Hxdetect.ShellDetector.init(options)
    
def Record(options):
    global record
    print 'RECORDING NOW,PLEASE WAIT\n'
    if options.directory:
        all_the_text = options.directory
    else:
        file_object = open(absPath+'//config//scan_dir')
        try:
            all_the_text = file_object.read( )
        finally:
            file_object.close( )
            all_the_text = all_the_text.strip('\n')
    GetValue(all_the_text,True,options.log)
    file_object = open(absPath+'//record//record', 'w')
    file_object.write(record)
    record = ''
    file_object.close()
    print record
    print 'RECORD FINISHED'   

def Detect(file):
    global _tot
    _tot += 1
    return Hxdetect.ShellDetector.anaylize(file)

def Scan(options):
    global record
    if os.path.exists(absPath+'//log//log'):
                filesz = os.path.getsize(absPath+'//log//log')
                if filesz > 83886080:
                    os.remove(absPath+'//log//log')
    print 'SCANNING WEBSHELL NOW,PLEASE WAIT\n'
    
    if options.directory:
        all_the_text = options.directory
    else:
        file_object = open(absPath+'//config//scan_dir')
        try:
            all_the_text = file_object.read( )
        finally:
            file_object.close( )
            all_the_text = all_the_text.strip('\n')
    
    if  True:
        client.doInCloud(all_the_text)
        
    GetValue(all_the_text,False,options.log)
    
    file_object = open(absPath+'//temp//record', 'w')
    file_object.write(record)
    record = ''
    file_object.close()
    file_now = open(absPath+'//temp//record')
    file_past_list = []
    file_past = open(absPath+'//record//record')
    for linez in file_past:
        file_past_list.append(linez)
    file_past.close()
    
    for line in file_now:
        flagz = False
#        file_past = open(absPath+'//record//record')
        fineRecord = False;
        for linez in file_past_list:
            if fineRecord == False:
                fineRecord = True
            if line.strip() == linez.strip():
                flagz = True
                break
        if fineRecord == False:    
            Record(options)
#            file_past.close()
#            file_past = open(absPath+'//record//record')
#            for linez in file_past:
#                if line == linez:
#                    flagz = True
#                    break
            break
        if flagz == True:
#            file_past.close()
            continue
        else:
#            file_past.close()
            correctFile = True
            correctFile = Detect(line.split('+')[0])
            if correctFile == True:    
                record = "%s+%s\n" % (line.split('+')[0],str(SHA1FileWithName(line.split('+')[0])))
                file_past = open(absPath+'//record//record', 'a')
                file_past.write(record)
                file_past.close()
                record = ''
            else:
                if options.log:
                    Log(line.split('+')[0],line.split('+')[1])
    file_now.close()
    print 'SCAN FINISHED'

def Log(content,sha):
    try:
        output = open(absPath+'//log//log', 'a')
        output.write('POSSIBLE WEBSHELL:'+content+'\nSHA1:'+sha+time.strftime( ISOTIMEFORMAT, time.localtime() )+'\n')
        output.close()
    finally:
        output.close()

def Kill(options):
    global record
    if os.path.exists(absPath+'//log//log'):
                filesz = os.path.getsize(absPath+'//log//log')
                if filesz > 83886080:
                    os.remove(absPath+'//log//log')
    print 'KILLING WEBSHELL NOW,PLEASE WAIT\n'
    file_object = open(absPath+'//config//scan_dir')
    try:
        all_the_text = file_object.read( )
    finally:
        file_object.close( )
    all_the_text = all_the_text.strip('\n')
    GetValue(all_the_text,False,options.log)
    file_object = open(absPath+'//temp//record', 'w')
    file_object.write(record)
    record = ''
    file_object.close()
    file_now = open(absPath+'//temp//record')
    for line in file_now:
        flagz = False
        file_past = open(absPath+'//record//record')
        for linez in file_past:
            if line == linez:
                flagz = True
                break
        if flagz == True:
            file_past.close()
            continue
        else:
            file_past.close()
            Detect(line.split('+')[0])
            if options.log:
                Log(line.split('+')[0],line.split('+')[1])
            os.remove(line.split('+')[0])
    print 'KILL FINISHED'

def Status():
    file_object = open(absPath+'//config//scan_dir')
    try:
        all_the_text = file_object.read( )
    finally:
        file_object.close( )
    if (all_the_text == ''):
        all_the_text = 'WAIT TO ADD'
    print 'WEBSITE DIRECTORY TO SCAN:\n'+all_the_text+'\n'
    file_object = open(absPath+'//config//scan_extensions')
    try:
        all_the_text = file_object.read( )
    finally:
        file_object.close( )
    if (all_the_text == ''):
        all_the_text = 'WAIT TO ADD'
    print 'FILE EXTENSIONS TO SCAN:\n'+all_the_text+'\n'
    file_object = open(absPath+'//config//whitelist_dir')
    try:
        all_the_text = file_object.read( )
    finally:
        file_object.close( )
    if (all_the_text == ''):
        all_the_text = 'WAIT TO ADD'
    print 'WHITELIST TO SKIP:\n'+all_the_text+'\n'
    
def Other():
    print '\nHOW TO USE:\n'
    print '1.Complete the configuration refer to the simple:'
    print '2.Use "-m rec" to take notes of the SHA1 of WEBSITE files.If you have modified the WEBSITE files,You have to use "-rec" to take notes of the SHA1 of these files again.'
    print '3.Use "-m scan" to scan the webshell files'
    print '4.Use "-m kill" to kill the webshell files(Program will kill webshell automatically without notification)'
    print '5.Use "-m status" to show the status of configuration'
    print '6.Use "-m about" to show the software version\n'
    print 'MINT WEBSHELL DEFENDER DEVELOPED BY jkkj93'                 
if __name__ == "__main__": 
    global absPath
    absPath = os.path.split(os.path.realpath(sys.argv[0]))[0] 
    parser = optparse.OptionParser()
    parser.add_option('--directory', '-d', type="string", help="values for scan path,Also set in the config if you like, specify directory to scan")
    parser.add_option('--modele', '-m',  type="string", default="scan", help="values:sacan rec or kill, default rec ; scan the webshell files")
    parser.add_option('--output', '-o',  type="string", default=False, help="values:True,or False,default False ,if you choose True,'./output/report.html' will be found !")
    parser.add_option('--log', '-t',  default=False, help="values: Fault or True,default Fault ,any log? the log in './log/log' !")
    parser.add_option('--fileInfo', '-f', type="string", default=False, help="values: Fault or True,default Fault ,list more file Infomation but cost of time, comma separated")
  
    parser.add_option('--remote', '-r', default="False", help="NOW,unuserFul !!! get shells signatures db by remote")
    parser.add_option('--linenumbers', '-l', default=False, help="NOW,unuserFul !!!show line number where suspicious function used")

    (options, args) = parser.parse_args()
    
    init(options)
    
    bTime = None
    eTime = None
    
    record = ''
#    if len(sys.argv) == 2:
    if (options.modele.lower()  == 'status'):
        Status(options)
    elif (options.modele.lower() == 'rec'):
        Record(options)
    elif (options.modele.lower() == 'scan'):
        bTime = time.clock()
        Scan(options)
        eTime = time.clock()
        print "_TT"+str(_TT)+" _tot:"+str(_tot)
        Hxdetect.ShellDetector.printResult()
        print str(eTime - bTime) +" seconds"
        Hxdetect.ShellDetector.outputResult(options)
    elif (options.modele.lower() == 'kill'):
        Kill()
    elif (options.modele.lower() == 'about'):
        print 'WELCOME TO USE MINT WEBSHELL DEFENDER 1.0'
    else:
        Other()
    Hxdetect.ShellDetector.end(options)
    
    
def Test():
    global absPath
    absPath = os.path.split(os.path.realpath(sys.argv[0]))[0] 
    
    parser = optparse.OptionParser()
    parser.add_option('--directory', '-d', type="string", help="values for scan path,Also set in the config if you like, specify directory to scan")
    parser.add_option('--modele', '-m',  type="string", default="scan", help="values:sacan rec or kill, default rec ; scan the webshell files")
    parser.add_option('--output', '-o',  type="string", default=False, help="values:True,or False,default False ,if you choose True,'./output/report.html' will be found !")
    parser.add_option('--log', '-t',  default=False, help="values: Fault or True,default Fault ,any log? the log in './log/log' !")
    parser.add_option('--fileInfo', '-f', type="string", default=False, help="values: Fault or True,default Fault ,list more file Infomation but cost of time, comma separated")
  
    parser.add_option('--remote', '-r', default="False", help="NOW,unuserFul !!! get shells signatures db by remote")
    parser.add_option('--linenumbers', '-l', default=False, help="NOW,unuserFul !!!show line number where suspicious function used")

    (options, args) = parser.parse_args()
    
    init(options)
    bTime = None
    eTime = None
    
    record = ''
#    if len(sys.argv) == 2:
    if (options.modele.lower()  == 'status'):
        Status(options)
    elif (options.modele.lower() == 'rec'):
        Record(options)
    elif (options.modele.lower() == 'scan'):
        Scan(options)
        eTime = time.clock()
        Hxdetect.ShellDetector.outputResult(options)
        print "_TT"+str(_TT)+" _tot:"+str(_tot)
        Hxdetect.ShellDetector.printResult()
        print str(eTime - bTime) +" seconds"
    elif (options.modele.lower() == 'kill'):
        Kill()
    elif (options.modele.lower() == 'about'):
        print 'WELCOME TO USE MINT WEBSHELL DEFENDER 1.0'
    else:
        Other()
    Hxdetect.ShellDetector.end(options)
    
