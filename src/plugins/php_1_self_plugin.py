#/usr/bin/env python
#coding=utf8
import os
import sys
import hashlib
import re
import time
import Hxdetect
import optparse
import datetime
import traceback  
rule =[
        'function\_exists\s*\(\s*[\'|\"](popen|exec|proc\_open|system|passthru)+[\'|\"]\s*\)',
        '(exec|shell\_exec|system|passthru)+\s*\(\s*\$\_(\w+)\[(.*)\]\s*\)',
        '((udp|tcp)\:\/\/(.*)\;)+',
        'preg\_replace\s*\((.*)\/e(.*)\,\s*\$\_(.*)\,(.*)\)',
        'preg\_replace\s*\((.*)\(base64\_decode\(\$',
        '(eval|assert|include|require|include\_once|require\_once)+\s*\(\s*(base64\_decode|str\_rot13|gz(\w+)|file\_(\w+)\_contents|(.*)php\:\/\nput)+',
        '(eval|assert|include|require|include\_once|require\_once|array\_map|array\_walk)+\s*\(\s*\$\_(GET|POST|REQUEST|COOKIE|SERVER|SESSION)+\[(.*)\]\s*\)',
        'eval\s*\(\s*\(\s*\$\$(\w+)',
        
        '(include|require|include\_once|require\_once)+\s*\(\s*[\'|\"](\w+)\.(jpg|gif|ico|bmp|png|txt|zip|rar|htm|css|js)+[\'|\"]\s*\)',
        '\$\_(\w+)(.*)(eval|assert|include|require|include\_once|require\_once)+\s*\(\s*\$(\w+)\s*\)',
        '\(\s*\$\_FILES\[(.*)\]\[(.*)\]\s*\,\s*\$\_(GET|POST|REQUEST|FILES)+\[(.*)\]\[(.*)\]\s*\)',
        '(fopen|fwrite|fputs|file\_put\_contents)+\s*\((.*)\$\_(GET|POST|REQUEST|COOKIE|SERVER)+\[(.*)\](.*)\)',
        'echo\s*curl\_exec\s*\(\s*\$(\w+)\s*\)',
        
        'new com\s*\(\s*[\'|\"]shell(.*)[\'|\"]\s*\)',
#        '\$(.*)\s*\((.*)\/e(.*)\,\s*\$\_(.*)\,(.*)\)',
        '\$\_\=(.*)\$\_',
        
        '\$\_(GET|POST|REQUEST|COOKIE|SERVER)+\[(.*)\]\(\s*\$(.*)\)',
        '\$(\w+)\s*\(\s*\$\_(GET|POST|REQUEST|COOKIE|SERVER)+\[(.*)\]\s*\)',
        '\$(\w+)\s*\(\s*\$\{(.*)\}',
        '\$(\w+)\s*\(\s*chr\(\d+\)'
        ]
def  judgeBackdoor(fileCtent):
    _match = []
    for r in rule:
        _match = re.compile(r).findall(fileCtent)
        if _match:                
            return 'backdoor,RULE:1_self'

    return None


#_content = open("D:\\E\\webshell-sample-master-91ef86ed3d642a53b0adbead8befe8daa21544f2webshell-sample.git\\asp\\11f940a7ca490fa3babca07a7a032440f87e8405.asp", 'rt', -1).read()
#judgeBackdoor(_content) 


#if re.compile('\$(.*)\s*\((.*)\/e(.*)\,\s*\$\_(.*)\,(.*)\)').findall("$12  (we\/ewe,  $_we,we)"):                
#    print 'bingo'