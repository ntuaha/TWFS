# -*- coding: utf-8 -*- 

import xlrd
import re

#處理掉unicode 和 str 在ascii上的問題
import sys 
import os
reload(sys) 
sys.setdefaultencoding('utf8') 


def parse(source_path,destination_path,date):
	book = xlrd.open_workbook(source_path+date+".xls")
	sh = book.sheet_by_index(0)

	bank_data = {}
	header=['年月','銀行','銀行類別','項目','數值']
	rows = []
	total_data = [None]*10
	jump_gap = 8
	mode  = 0
	modelist = ['國內銀行','國外銀行','信用合作社']
	for i in range(sh.nrows):
		row_name = unicode(sh.cell_value(rowx=i,colx = 0))
		if unicode(sh.cell_value(rowx=i,colx = 1)) == u"":	
			#空的但是資料開頭就跳到資料頭		
			if  row_name == u"2-1　一般銀行及信用合作社存款月底餘額":
				mode =1
			#	
			if row_name == u"2-1　一般銀行及信用合作社存款月底餘額（續二）":
				mode =2
			if row_name == u"2-1　一般銀行及信用合作社存款月底餘額（續四）":
				mode =3
			#print "%d: Empty:%s" %(i,row_name)
			continue
		
		#第二藍衛如果是文字就跳過
		if len(re.findall(r"[-+]?\d*\.\d+|\d+",unicode(sh.cell_value(rowx=i,colx = 1)))) == 0:
			continue

	
		if row_name== u"總　　　　　計　Total":
			total_data[0] = date
			total_data[1] = int(float(sh.cell_value(rowx=i,colx = 1))*1e6)
			total_data[2] = int(float(sh.cell_value(rowx=i,colx = 2))*1e6)
			total_data[3] = int(float(sh.cell_value(rowx=i,colx = 3))*1e6)
			total_data[4] = int(float(sh.cell_value(rowx=i,colx = 4))*1e6)
			rows.append([total_data[0],"總計",modelist[mode-1],'活期存款',total_data[1]])
			rows.append([total_data[0],"總計",modelist[mode-1],'定期存款',total_data[2]])
			rows.append([total_data[0],"總計",modelist[mode-1],'外匯存款',total_data[3]])
			rows.append([total_data[0],"總計",modelist[mode-1],'公股存款與其他',total_data[4]])
			
		else:
			bank_name = unicode(sh.cell_value(rowx=i,colx = 0))
			bank_name = re.split('[\W+|(]', bank_name, flags=re.U)[0]
			bank_data[bank_name] = {}
			bank_data[bank_name]["ALL_MD"] = int(float(sh.cell_value(rowx=i,colx = 1))*1e6)
			bank_data[bank_name]["ALL_FD"] = int(float(sh.cell_value(rowx=i,colx = 2))*1e6)
			bank_data[bank_name]["ALL_FY"] = int(float(sh.cell_value(rowx=i,colx = 3))*1e6)			
			bank_data[bank_name]["ALL_LD"] = int(float(sh.cell_value(rowx=i,colx = 4))*1e6)			
			rows.append([total_data[0],bank_name,modelist[mode-1],"活期存款",bank_data[bank_name]["ALL_MD"]])
			rows.append([total_data[0],bank_name,modelist[mode-1],"定期存款",bank_data[bank_name]["ALL_FD"]])
			rows.append([total_data[0],bank_name,modelist[mode-1],'外匯總存款',bank_data[bank_name]["ALL_FY"]])
			rows.append([total_data[0],bank_name,modelist[mode-1],'公股存款與其他',bank_data[bank_name]["ALL_LD"]])
	#將資料寫入csv
	output(destination_path,header,date,rows)


def parse2(source_path,destination_path,date):
	book = xlrd.open_workbook(source_path+date+".xls")
	print "The number of worksheets is",book.nsheets
	print "Worksheet name(s):", book.sheet_names()
	modes = [1,1,1,2,2,2,3,4,4]
	bank_data = {}
	total_data = [None]*10
	header=['年月','銀行','項目','數值']
	rows = []
	total_data[0] = date
	modelist = ['國內銀行','外國銀行在臺分行（含OBU）','大陸地區銀行在臺分行','信用合作社']
	for sheet_num in range(book.nsheets):
		sh = book.sheet_by_index(sheet_num)
		mode  = modes[sheet_num]
		for i in range(sh.nrows):
			row_name = unicode(sh.cell_value(rowx=i,colx = 0))
			if unicode(sh.cell_value(rowx=i,colx = 1)) == u"":	
				continue
			
			#第二藍衛如果是文字就跳過
			if len(re.findall(r"[-+]?\d*\.\d+|\d+",unicode(sh.cell_value(rowx=i,colx = 1)))) == 0:
				continue

			if row_name== u"總　　　　　計":
				total_data[0] = date
				total_data[1] = int(float(sh.cell_value(rowx=i,colx = 1))*1e6)
				total_data[2] = int(float(sh.cell_value(rowx=i,colx = 2))*1e6)
				total_data[3] = int(float(sh.cell_value(rowx=i,colx = 3))*1e6)
				total_data[4] = int(float(sh.cell_value(rowx=i,colx = 4))*1e6)
				rows.append([total_data[0],"總計",modelist[mode-1],'活期存款',total_data[1]])
				rows.append([total_data[0],"總計",modelist[mode-1],'定期存款',total_data[2]])
				rows.append([total_data[0],"總計",modelist[mode-1],'外匯存款',total_data[3]])
				rows.append([total_data[0],"總計",modelist[mode-1],'公股存款與其他',total_data[4]])
				
			else:
				bank_name = unicode(sh.cell_value(rowx=i,colx = 0))
				bank_name = re.split('[\W+|(]', bank_name, flags=re.U)[0]
				bank_data[bank_name] = {}
				bank_data[bank_name]["ALL_MD"] = int(float(sh.cell_value(rowx=i,colx = 1))*1e6)
				bank_data[bank_name]["ALL_FD"] = int(float(sh.cell_value(rowx=i,colx = 2))*1e6)
				bank_data[bank_name]["ALL_FY"] = int(float(sh.cell_value(rowx=i,colx = 3))*1e6)			
				bank_data[bank_name]["ALL_LD"] = int(float(sh.cell_value(rowx=i,colx = 4))*1e6)			
				rows.append([total_data[0],bank_name,modelist[mode-1],"活期存款",bank_data[bank_name]["ALL_MD"]])
				rows.append([total_data[0],bank_name,modelist[mode-1],"定期存款",bank_data[bank_name]["ALL_FD"]])
				rows.append([total_data[0],bank_name,modelist[mode-1],'外匯總存款',bank_data[bank_name]["ALL_FY"]])
				rows.append([total_data[0],bank_name,modelist[mode-1],'公股存款與其他',bank_data[bank_name]["ALL_LD"]])
	#將資料寫入csv
	output(destination_path,header,date,rows)
				


#輸出
def output(destination_path,header,date,data):
	f = open("%s%s.csv"%(destination_path,date),"w+")
	f.write(",".join(header)+"\n")
	for d in data:
		try:
			f.write(",".join(map(str,d))+"\n")
		except KeyError:
			f.write(",".join(map(str,d))+"\n")
	f.close()
	print date
	
def checkFolder(folder):
	if os.path.exists(folder) == False:
		os.makedirs(folder)



def parser(date):
	folder = 'MD_Bal'
	from_path= '/Users/aha/Dropbox/Project/Financial/Plan/rawdata/%s/' % (folder)
	to_path = '/Users/aha/Dropbox/Project/Financial/Plan/data/%s/' % (folder)
	#from_path= '/home/aha/Data/TWFS/rawdata/%s/' % (folder)
	#to_path = '/home/aha/Data/TWFS/data/%s/' % (folder)
	checkFolder(to_path)
 	parse(from_path,to_path,date)

def parser2(date):
	folder = 'MD_Bal'
	from_path= '/Users/aha/Dropbox/Project/Financial/Plan/rawdata/%s/' % (folder)
	to_path = '/Users/aha/Dropbox/Project/Financial/Plan/data/%s/' % (folder)
	#from_path= '/home/aha/Data/TWFS/rawdata/%s/' % (folder)
	#to_path = '/home/aha/Data/TWFS/data/%s/' % (folder)
	checkFolder(to_path)
 	parse2(from_path,to_path,date)

def parserAll():
	folder = 'MD_BAL'
	from_path= '/home/aha/Data/TWFS/rawdata/%s/' % (folder)
	to_path = '/home/aha/Data/TWFS/data/%s/' % (folder)
	checkFolder(to_path)

	for yy in range(95,100):
		for mm in range(1,13):
			date = '%d%02d'%(yy,mm)
			parse(from_path,to_path,date)
	parse(from_path,to_path,'10101')
	for yy in range(100,101):
		for mm in range(2,13):
			date = '%d%02d'%(yy,mm)
			parse2(from_path,to_path,date)
	for yy in range(101,103):
		for mm in range(1,13):
			date = '%d%02d'%(yy,mm)
			parse2(from_path,to_path,date)


if __name__ == '__main__':
	parserAll()
	#parser('9908')
	#parser2('10205')
	


