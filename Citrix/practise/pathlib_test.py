from pathlib import Path
path = Path('../classify')
file = path/'a.py'
with open(file,'r',encoding='utf-8') as f:
    content = f.readlines()

#print(content)
#print(type(content)) #=>list
# content2 = file.read_text(encoding='utf-8')
# print(type(content2)) #=>str
