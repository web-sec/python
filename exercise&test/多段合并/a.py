s = ''
with open('a.txt','r') as fr:
    for line in fr.readlines():
        lineArr = line.strip()
        s+=lineArr

with open('b.txt','w') as fr:
    fr.write(s)
