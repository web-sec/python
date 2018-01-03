#/usr/bin/env python
#coding=utf8

import re
import os

def  judgeBackdoor(fileCtent):
	if fileCtent[:-4] == 'Zend':
#		if os.path.getsize(filepath) == 178:
			return 'zend加密php一句话后门'
#		return None
	return None