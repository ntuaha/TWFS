# -*- coding: utf-8 -*- 

import re

#處理掉unicode 和 str 在ascii上的問題
import sys 
import os
import pg
import DB_INFO
reload(sys) 
sys.setdefaultencoding('utf8') 

				
def insert(table,data):

	print DB_INFO.database
	#conn = pg.connect(DB_INFO.database,DB_INFO.server_site,DB_INFO.port,None,None,DB_INFO.username,DB_INFO.password)
	#ds = conn.query("select * from table1")
	#conn.disconnect()
	print data


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
			year = int(row[0][0:3])+1911
			month = int(row[0][3:5])
			date = "%d-%d-01" % (year,month)
			data[row[1]] = row[2]
		data["date"] = date
	f.close()
	insert(None,data)





 		




if __name__ == '__main__':
	path = '/Users/aha/Dropbox/Project/Financial/Plan/data/PESI/'
	read("%s%d.csv"%(path,10206))

