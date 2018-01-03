#/usr/bin/env python
#coding=utf8

import re

rule =['@\$\_\(\$\_',
 
'\$\_=\"\"',
 
'\${\'\_\'',
 
'@preg\_replace\((\")*\/(\S)*\/e(\")*,\$_POST\[\S*\]',
 
'base64\_decode\(\$\_',
 
'\'e\'\.\'v\'\.\'a\'\.\'l\'',
 
'\"e\"\.\"v\"\.\"a\"\.\"l\"',
 
'\"e\"\.\"v\"\.\"a\"\.\"l\"',
 
'\$(\w)+\(\"\/(\S)+\/e',
 
'\(array\)\$_(POST|GET|REQUEST|COOKIE)',
 
'\$(\w)+\(\${',    
 
'@\$\_=',
 
'\$\_=\$\_',    
 
'chr\((\d)+\)\.chr\((\d)+\)',
 
'phpjm\.net',
 
'cha88\.cn',
 
'c99shell',
 
'phpspy',
 
'Scanners',
 
'cmd\.php',
 
'str_rot13',
 
'webshell',
 
'EgY_SpIdEr',
 
'tools88\.com',
 
'SECFORCE',
 
'eval\((\'|")\?>',
 
'preg_replace\(\"\/\.\*\/e\"',
 
'assert\((\'|"|\s*)\\$',
 
'eval\(gzinflate\(',
'gzinflate\(base64_decode\(',
 
'eval\(base64_decode\(',
 
'eval\(gzuncompress\(',
 
'ies\",gzuncompress\(\$',
 
'eval\(gzdecode\(',
 
'eval\(str_rot13\(',
 
'gzuncompress\(base64_decode\(',
 
'base64_decode\(gzuncompress\(',
 
'eval\((\'|"|\s*)\\$_(POST|GET|REQUEST|COOKIE)',
 
'assert\((\'|"|\s*)\\$_(POST|GET|REQUEST|COOKIE)',
 
'require\((\'|"|\s*)\\$_(POST|GET|REQUEST|COOKIE)',
 
'require_once\((\'|"|\s*)\\$_(POST|GET|REQUEST|COOKIE)',
 
'include\((\'|"|\s*)\\$_(POST|GET|REQUEST|COOKIE)',
 
'include_once\((\'|"|\s*)\\$_(POST|GET|REQUEST|COOKIE)',       
 
'call_user_func\(("|\')assert("|\')',          
 
'call_user_func\((\'|"|\s*)\\$_(POST|GET|REQUEST|COOKIE)',
 
'\$_(POST|GET|REQUEST|COOKIE)\[([^\]]+)\]\((\'|"|\s*)\\$_(POST|GET|REQUEST|COOKIE)\[', 
 
'echo\(file_get_contents\((\'|"|\s*)\\$_(POST|GET|REQUEST|COOKIE)',                    
'file_put_contents\((\'|"|\s*)\\$_(POST|GET|REQUEST|COOKIE)\[([^\]]+)\],(\'|"|\s*)\\$_(POST|GET|REQUEST|COOKIE)',
'fputs\(fopen\((.+),(\'|")w(\'|")\),(\'|"|\s*)\\$_(POST|GET|REQUEST|COOKIE)\[',
 
'SetHandlerapplication\/x-httpd-php',
 
'php_valueauto_prepend_file',
 
'php_valueauto_append_file']
def  judgeBackdoor(fileCtent):
	_match = []
	for r in rule:
	    _match = re.compile(r).findall(fileCtent)
	    if _match:                
	        return 'backdoor,RULE:2_self'
	return None