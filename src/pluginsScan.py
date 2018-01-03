#!/usr/bin/env python
#coding=utf8


import os, glob, sys
import time
#from plugins import php_array_map
#from plugins import php_array_map_plugin
#from plugins import php_call_user_func
#from plugins import php_eval_assert_plugin
#from plugins import php_include_file_plugin
#from plugins import php_packshell_plugin

#插件列表
plusArr = [] 

#加载插件
def loadPlus(ext="all"):
	plusTmp = glob.glob('plugins/*_plugin.py')
	if ext == "all":
		for plus in plusTmp:
			#plusname = plus.split('\\')[-1][:-3]
			plusname = plus.replace('\\\\','/').replace('\\','/').replace('/','.').replace('.py','')
    			__import__(plusname)
			plusArr.append(plusname)
	elif ext == "php":
		for plus in plusTmp:
			plusname = plus.split('/')[-1][:-3]
			if plusname.find("php") == 0:
				__import__("plugins." + plusname)
				plusArr.append(plusname)
	elif ext == "asp":
		for plus in plusTmp:
			plusname = plus.split('/')[-1][:-3]
			if plusname.find("aps") == 0:
				__import__("plugins." + plusname)
				plusArr.append(plusname)
	elif ext == "aspx":
		for plus in plusTmp:
			plusname = plus.split('/')[-1][:-3]
			if plusname.find("apsx") == 0:
				__import__("plugins." + plusname)
				plusArr.append( plusname)
	elif ext == "jsp":
		for plus in plusTmp:
			plusname = plus.split('/')[-1][:-3]
			if plusname.find("jps") == 0:
				__import__("plugins." + plusname)
				plusArr.append(plusname)
	else:
		print "error args!"
		exit()

#通过加载插件扫描
def detectPlus(fileCtent):
	res = None
	for plus in plusArr:
		res = sys.modules[plus].judgeBackdoor(fileCtent)
		if res:
			break
		else:
			pass
	return res	
