# -*- coding: utf-8 -*-
import sqlite3

def connectdb(name):
  global conn
  conn = sqlite3.connect(name)
  return conn.cursor()

def showtable(cur):
  ret = cur.execute('select name from sqlite_master')
  for name in ret:
    print name[0]

def desc(cur,name):
  t = (name,)
  ret = cur.execute('select sql from sqlite_master where name=?',t)
  for sql in ret:
    print sql[0]

if __name__=="__main__":
  pass