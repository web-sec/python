#!/usr/bin/env python
#coding=utf8

head = '<!doctype html><html><head><meta http-equiv="Content-Type" content="text/html" charset="utf8"><meta charset="UTF-8"></head>\
		<h1 style="text-align:center">webshell后门报告</h1>\
		<div style="text-align:center"><table border="1" style="margin:auto; width:%90;">\
		<tr><th>路径</th><th>类型</th></tr>'

def createHtml(resList):
	tr = ''
	for res in resList:
		tmp = ''
		for ele in res:
			tmp += '<td>' + ele +'</td>'
		tr += '<tr>' + tmp + '</tr>'
	html = head + tr + '</table></div></html>'
	return html
