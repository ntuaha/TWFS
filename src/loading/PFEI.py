# -*- coding: utf-8 -*- 

import xlrd
import re

#處理掉unicode 和 str 在ascii上的問題
import sys 
import os
reload(sys) 
sys.setdefaultencoding('utf8') 

				
def insert(table,data):
	pass


def read(source_path):
	f = open(source_path,"r")
	while 1:
		lines = f.readlines(10000)
		if not liens:
			break
		for line in lines:
			row = line.split(',')
			print row
	f.close()





 		




if __name__ == '__main__':
	from_path= '/Users/aha/Dropbox/Project/Financial/Data/'
	to_path = '/Users/aha/Dropbox/Project/Financial/Codes/csv/'
	cmd = "rm %sTotal.csv"%(to_path)
	os.system(cmd)

	f = open("%sTotal.csv"%(to_path),"a+")
	total_header = ['年月','全行外匯活期存款','全行外匯定期存款','全行總額','國內外匯活期存款','國內外匯定期存款','國內總額','海外外匯活期存款','海外外匯定期存款','海外總額']
	f.write(",".join(total_header)+"\n")
	f.close()
	yy = 95
	mm = 1
	for yy in range(95,100):
		for mm in range(1,13):
			date = '%d%02d'%(yy,mm)
			parse(from_path,to_path,date)
	parse(from_path,to_path,'10001')


