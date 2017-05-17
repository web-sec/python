#!python3
#-*-coding:utf-8-*-
a={'a':1,'b':2,'c':3}

if __name__=='__main__':
    if 'a' in a:
        a.pop('a')
    print(a)
