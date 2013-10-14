# -*- coding: utf-8 -*- 

import re

#處理掉unicode 和 str 在ascii上的問題
import sys 
import os
#import pg
#import DB_INFO
import psycopg2


reload(sys) 
sys.setdefaultencoding('utf8') 

				
def insert(table,data):

	#print DB_INFO.database
	#conn = pg.connect(DB_INFO.database,DB_INFO.server_site,DB_INFO.port,None,None,DB_INFO.username,DB_INFO.password)
	#ds = conn.query("select * from table1")
	#conn.disconnect()
	print data

def makeSQL(date,data):
	r = data
	#print r.keys()
	#print date
	del r["Bund_Txn_Amt_TY"]
	k = r.keys()
	li = [r[index] for index in k]
	cols  = ','.join(k)
	values = ','.join(li)
	#conn = pg.connect(DB_INFO.database,DB_INFO.server_site,DB_INFO.port,None,None,DB_INFO.username,DB_INFO.password)
	#conn = pg.connect('data','localhost',5432,None,None,'aha','dataaha305')
	conn = psycopg2.connect(database="data", user="aha", password="dataaha305", host="127.0.0.1", port="5432")
	cur = conn.cursor()
	#ds = conn.query("DELETE FROM PFEI WHERE Data_Ym='%s'"%(date))
	cur.execute("DELETE FROM PFEI WHERE Data_Ym='%s'"%(date))
	sql = "INSERT INTO PFEI (Data_Ym,%s) VALUES (Timestamp '%s',%s)" %(cols,date,values)
	#print sql
	#conn.query(sql)
	cur.execute(sql)
	conn.commit()
	cur.execute("SELECT * FROM PFEI")
	rows = cur.fetchall()
	# for row in rows:
	# 	for i in row:
	# 		print "{:20.2F}".format(i)
	# 	print "\n"

    

	conn.close()

def read(source_path):
	f = open(source_path,"r")
	header = f.readline()
	data = {}
	date = None
	while 1:
		lines = f.readlines(10000)
		if not lines:
			break		
		for line in lines:
			row = line.split(',')
			year = int(row[0][:-2])+1911
			month = int(row[0][-2:])
			date = "%d-%d-01" % (year,month)
			data[row[3][:-1]] = row[2]
		#data["date"] = date
	f.close()
	print date
	makeSQL(date,data)

def runAll(path):
	for yy in range(95,103):
		for mm in range(1,13):
			read("%s%d%02d.csv"%(path,yy,mm))

if __name__ == '__main__':
	path = '/home/aha/Data/TWFS/data/PFEI/'
	#read("%s%d.csv"%(path,10206))
	runAll(path)

