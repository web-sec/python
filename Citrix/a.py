#coding:utf-8
import csv
w = [[1],[2],[3],[4],[5]]
with open('../info/test.csv','w',newline ='') as f:
    writer = csv.writer(f)
    for i in w:
        writer.writerow(i)
