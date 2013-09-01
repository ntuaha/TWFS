# -*- coding: utf-8 -*- 
import parse
import parse2
import os
 		




if __name__ == '__main__':
	from_path= '/Users/aha/Dropbox/Project/Financial/Data/'
	to_path = '/Users/aha/Dropbox/Project/Financial/Codes/csv/'
	cmd = "rm %sTotal.csv"%(to_path)
	os.system(cmd)

	f = open("%sTotal.csv"%(to_path),"a+")
	total_header = ['年月','全行外匯活期存款','全行外匯定期存款','全行總額','國內外匯活期存款','國內外匯定期存款','國內總額','海外外匯活期存款','海外外匯定期存款','海外總額']
	f.write(",".join(total_header)+"\n")
	f.close()

#Use parse.py to extract data from xls to csv before 2011.2
	for yy in range(95,100):
		for mm in range(1,13):
			date = '%d%02d'%(yy,mm)
			parse.parse(from_path,to_path,date)
	parse.parse(from_path,to_path,'10001')

#Use parse2.py to extract data from xls to csv 2011.2 - now
	for mm in range(2,13):
		date = '%d%02d'%(100,mm)
		parse2.parse(from_path,to_path,date)
	for mm in range(1,13):
		date = '%d%02d'%(101,mm)
		parse2.parse(from_path,to_path,date)
	for mm in range(1,13):
		date = '%d%02d'%(102,mm)
		parse2.parse(from_path,to_path,date)		
	#parse2.parse(from_path,to_path,'10201')
	#parse2.parse(from_path,to_path,'10202')




