#coding: utf-8

"""
キャッシュをsqlite3で管理するモジュール
"""
import sqlite3
import datetime

con = sqlite3.connect("cache.db")
cur = con.cursor()

def getContent(url):
	ret = cur.execute("""select content from cache where url = ?""",(url,))
	return ret.fetchone()
	
def setContent(url,content):
	cur.execute("""insert into cache values (?,?,?)""",(url,content,str(datetime.datetime.now())))
	con.commit()
	
if __name__=="__main__":
	pass