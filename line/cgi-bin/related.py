#!/usr/bin/env python 
# -*- coding: utf-8 -*-

"""
指定されたURLから関連ニュース(div.mainBody>ul)にあたる部分だけを取得する
cssselectモジュールに依存
"""

import cgi
import urllib2
import lxml.html
import dbcache 

# ヘッダ
print "Content-type : text/html ; charset=utf-8"
print

form = cgi.FieldStorage()
content = ''
url = ''
try:
	url = form.getfirst("url","")
	cache = dbcache.getContent(url)
	if cache :
		content += cache[0]
	else:
		# URLから関連ニュースを取ってくる
		html = urllib2.urlopen(url).read()
		root = lxml.html.fromstring(html)
		section = root.cssselect('div.mainBody>ul')
		if  section != [] :
			msg = lxml.html.tostring(section[0])	
			content += msg
			dbcache.setContent(url,msg)
		else :
			dbcache.setContent(url,'')	
		# HTMLそのまま表示
	print content
except:
	pass
	
