#/usr/bin/env python
#coding=utf8

import re

rule =r"(?si)(function\_exists\s*\(\s*[\'|\"](popen|exec|proc\_open|system|passthru)+[\'|\"]\s*\)|(exec|shell\_exec|system|passthru)+\s*\(\s*\$\_(\w+)\[(.*)\]\s*\)|((udp|tcp)\:\/\/(.*)\;)+|preg\_replace\s*\((.*)\/e(.*)\,\s*\$\_(.*)\,(.*)\)|preg\_replace\s*\((.*)\(base64\_decode\(\$|(eval|assert|include|require|include\_once|require\_once)+\s*\(\s*(base64\_decode|str\_rot13|gz(\w+)|file\_(\w+)\_contents|(.*)php\:\/\nput)+|(eval|assert|include|require|include\_once|require\_once|array\_map|array\_walk)+\s*\(\s*\$\_(GET|POST|REQUEST|COOKIE|SERVER|SESSION)+\[(.*)\]\s*\)|eval\s*\(\s*\(\s*\$\$(\w+)|(include|require|include\_once|require\_once)+\s*\(\s*[\'|\"](\w+)\.(jpg|gif|ico|bmp|png|txt|zip|rar|htm|css|js)+[\'|\"]\s*\)|\$\_(\w+)(.*)(eval|assert|include|require|include\_once|require\_once)+\s*\(\s*\$(\w+)\s*\)|\(\s*\$\_FILES\[(.*)\]\[(.*)\]\s*\,\s*\$\_(GET|POST|REQUEST|FILES)+\[(.*)\]\[(.*)\]\s*\)|(fopen|fwrite|fputs|file\_put\_contents)+\s*\((.*)\$\_(GET|POST|REQUEST|COOKIE|SERVER)+\[(.*)\](.*)\)|echo\s*curl\_exec\s*\(\s*\$(\w+)\s*\)|new com\s*\(\s*[\'|\"]shell(.*)[\'|\"]\s*\)|\$(.*)\s*\((.*)\/e(.*)\,\s*\$\_(.*)\,(.*)\)|\$\_\=(.*)\$\_|\$\_(GET|POST|REQUEST|COOKIE|SERVER)+\[(.*)\]\(\s*\$(.*)\)|\$(\w+)\s*\(\s*\$\_(GET|POST|REQUEST|COOKIE|SERVER)+\[(.*)\]\s*\)|\$(\w+)\s*\(\s*\$\{(.*)\}|\$(\w+)\s*\(\s*chr\(\d+\))"
def  judgeBackdoor(fileCtent):
	if re.compile(rule).findall(fileCtent):                
	        return 'bingo'
	return None