#-*-coding:utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import threading
from time import ctime,sleep

def music(func):
    for i in range(2):
        print "I was listening to %s. %s\n" %(func,ctime())
        sleep(1)

def move(func):
    for i in range(2):
        print "I was at the %s! %s\n" %(func,ctime())
        sleep(5)

threads = []
t1 = threading.Thread(target=music,args=(u'曹操',))
threads.append(t1)
t2 = threading.Thread(target=move,args=(u'银河护卫队',))
threads.append(t2)

if __name__ == '__main__':
    for t in threads:
        #t.setDaemon(True)#守护线程，当为子线程设置后，主线程完成任务后就会杀死子线程
        t.start()
    t.join()#等待子线程全都完成后才继续
    print("all over %s" %ctime())
