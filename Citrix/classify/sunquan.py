#!python3
#-*-coding:utf-8-*-
from bs4 import BeautifulSoup
import re
import requests



url = 'https://support.citrix.com/search?lang=en&ct=Technotes&prod=CitrixCloud&pver=&sort=relevance'
r = requests.get(url)
r.encoding = 'utf-8'
content = r.text
soup = BeautifulSoup(content,'html5lib')  # 解析器为lxml；python内置的为html.parser；还可以选html5lib(第三方库)


titles = []
ctx = []
data = []
a = soup.select('div.searchResult > ul > li > table > tbody > tr > td')
print(len(a))
for i in range(len(a)):
    if i%5==1:
        ctx.append(a[i].contents)
    if i%5==2:
        data.append(a[i].contents)

b = soup.select('div.searchResult > ul > li > h4 > a')
for i in b:
    titles.append(i.contents)

print(ctx)
print(data)
print(titles)



