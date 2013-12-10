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
	header=['年月','銀行','銀行類別','項目','數值','英文項目']
	column=["總外匯活期存款","總外匯定期存款","國內外匯活期存款","國內外匯定期存款","海外外匯活期存款","海外外匯定期存款"]
	columns_en = ["My_TOT","FY_TOT","My_Country","Fy_Country","MY_OS","FY_OS"]	
	rows = []
	#header = ['年月','銀行','銀行英文','全行外匯活期存款','全行外匯定期存款','全行總額','國內外匯活期存款','國內外匯定期存款','國內總額','海外外匯活期存款','海外外匯定期存款','海外總額','金控註記']
	total_data = [None]*10
	jump_gap = 8
	mode  = 0
	for i in range(sh.nrows):
		row_name = unicode(sh.cell_value(rowx=i,colx = 0))
		if unicode(sh.cell_value(rowx=i,colx = 1)) == u"":	
			#空的但是資料開頭就跳到資料頭		
			if  row_name == u"2-5　一般銀行外匯存款餘額":
				mode =1
			#	
			if row_name == u"2-5　一般銀行外匯存款餘額（續三）":
				mode =2
			#print "%d: Empty:%s" %(i,row_name)
			continue
		
		#第二藍衛如果是文字就跳過
		if len(re.findall(r"[-+]?\d*\.\d+|\d+",unicode(sh.cell_value(rowx=i,colx = 1)))) == 0:
			continue

		#全行總和
		if row_name== u"總　　　　　計　Total" and 1 == mode:
			total_data[0] = date
			total_data[1] = int(float(sh.cell_value(rowx=i,colx = 1))*1e6)
			total_data[2] = int(float(sh.cell_value(rowx=i,colx = 2))*1e6)
			total_data[3] = int(float(sh.cell_value(rowx=i,colx = 3))*1e6)
			rows.append([total_data[0],"總計",'全行外匯活期存款',column[0],total_data[1],columns_en[0]])
			rows.append([total_data[0],"總計",'全行外匯定期存款',column[1],total_data[2],columns_en[1]])
			#rows.append([total_data[0],"總計",'全行外匯總存款',total_data[3]])
			continue
		#全行銀行
		if 1 == mode:
			bank_name = unicode(sh.cell_value(rowx=i,colx = 0))
			bank_name = re.split('[\W+|(]', bank_name, flags=re.U)[0]
			bank_data[bank_name] = {}
			bank_data[bank_name]["ALL_MY"] = int(float(sh.cell_value(rowx=i,colx = 1))*1e6)
			bank_data[bank_name]["ALL_FY"] = int(float(sh.cell_value(rowx=i,colx = 2))*1e6)
			bank_data[bank_name]["ALL_Y"] = int(float(sh.cell_value(rowx=i,colx = 3))*1e6)			
			rows.append([total_data[0],bank_name,"全行外匯活期存款",column[0],bank_data[bank_name]["ALL_MY"],columns_en[0]])
			rows.append([total_data[0],bank_name,"全行外匯定期存款",column[1],bank_data[bank_name]["ALL_FY"],columns_en[1]])
			#rows.append([total_data[0],bank_name,'全行外匯總存款',bank_data[bank_name]["ALL_Y"]])


		#國內總和
		if sh.cell_value(rowx=i,colx = 0)== u"總　　　　　計　Total" and 2 == mode:
			#國內
			total_data[4] = int(float(sh.cell_value(rowx=i,colx = 1))*1e6)
			total_data[5] = int(float(sh.cell_value(rowx=i,colx = 2))*1e6)
			total_data[6] = int(float(sh.cell_value(rowx=i,colx = 3))*1e6)
			rows.append([total_data[0],"總計",'國內外匯活期存款',column[2],total_data[4],columns_en[2]])
			rows.append([total_data[0],"總計",'國內外匯定期存款',column[3],total_data[5],columns_en[3]])
			#rows.append([total_data[0],"總計",'國內外匯總存款',total_data[6]])
			#Oversea 海外
			total_data[7] = total_data[1] - total_data[4]
			total_data[8] = total_data[2] - total_data[5]
			total_data[9] = total_data[3] - total_data[6]
			rows.append([total_data[0],"總計",'海外外匯活期存款',column[4],total_data[7],columns_en[4]])
			rows.append([total_data[0],"總計",'海外外匯定期存款',column[5],total_data[8],columns_en[5]])
			#rows.append([total_data[0],"總計",'海外外匯總存款',total_data[9]])
			continue
		#國內銀行
		if 2 == mode:
			bank_name = unicode(sh.cell_value(rowx=i,colx = 0))
			bank_name = re.split('[\W+|(]', bank_name, flags=re.U)[0]
			bank_data[bank_name]["DB_MY"] = int(float(sh.cell_value(rowx=i,colx = 1))*1e6)
			bank_data[bank_name]["DB_FY"] = int(float(sh.cell_value(rowx=i,colx = 2))*1e6)
			bank_data[bank_name]["DB_Y"] = int(float(sh.cell_value(rowx=i,colx = 3))*1e6)
			bank_data[bank_name]["OS_MY"] = bank_data[bank_name]["ALL_MY"] - bank_data[bank_name]["DB_MY"]
			bank_data[bank_name]["OS_FY"] = bank_data[bank_name]["ALL_FY"] - bank_data[bank_name]["DB_FY"]
			bank_data[bank_name]["OS_Y"] = bank_data[bank_name]["ALL_Y"] - bank_data[bank_name]["DB_Y"]
			#print "%s %% %s" %(bank_data[bank_name],bank_name)
			rows.append([total_data[0],bank_name,'國內外匯活期存款',column[2],bank_data[bank_name]["DB_MY"],columns_en[2]])
			rows.append([total_data[0],bank_name,'國內外匯定期存款',column[3],bank_data[bank_name]["DB_FY"],columns_en[3]])
			#rows.append([total_data[0],bank_name,'國內外匯總存款',bank_data[bank_name]["DB_Y"]])
			rows.append([total_data[0],bank_name,'海外外匯活期存款',column[4],bank_data[bank_name]["OS_MY"],columns_en[4]])
			rows.append([total_data[0],bank_name,'海外外匯定期存款',column[5],bank_data[bank_name]["OS_FY"],columns_en[5]])
			#rows.append([total_data[0],bank_name,'海外外匯總存款',bank_data[bank_name]["OS_Y"]])

	output(destination_path,header,date,rows)


def parse2(source_path,destination_path,date):
	book = xlrd.open_workbook(source_path+date+".xls")
	#print "The number of worksheets is",book.nsheets
	#print "Worksheet name(s):", book.sheet_names()
	modes = [1,1,1,2,2,2]
	bank_data = {}
	#header = ['年月','銀行','銀行英文','全行外匯活期存款','全行外匯定期存款','全行總額','國內外匯活期存款','國內外匯定期存款','國內總額','海外外匯活期存款','海外外匯定期存款','海外總額','金控註記']
	total_data = [None]*10		
	header=['年月','銀行','銀行類別','項目','數值','英文項目']
	column=["總外匯活期存款","總外匯定期存款","國內外匯活期存款","國內外匯定期存款","海外外匯活期存款","海外外匯定期存款"]
	columns_en = ["My_TOT","FY_TOT","My_Country","Fy_Country","MY_OS","FY_OS"]	

	rows = []
	total_data[0] = date
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


			#全行總和
			if row_name== u"總　　　　　計" and 1 == mode:
				total_data[0] = date
				total_data[1] = int(float(sh.cell_value(rowx=i,colx = 1))*1e6)
				total_data[2] = int(float(sh.cell_value(rowx=i,colx = 2))*1e6)
				total_data[3] = int(float(sh.cell_value(rowx=i,colx = 3))*1e6)
				rows.append([total_data[0],"總計",'全行外匯活期存款',column[0],total_data[1],columns_en[0]])
				rows.append([total_data[0],"總計",'全行外匯定期存款',column[1],total_data[2],columns_en[1]])
				#rows.append([total_data[0],"總計",'全行外匯總存款',total_data[3]])
				continue
			#全行銀行
			if 1 == mode:
				bank_name = unicode(sh.cell_value(rowx=i,colx = 0))
				bank_name = re.split('[\W+|(]', bank_name, flags=re.U)[0]
				bank_data[bank_name] = {}
				bank_data[bank_name]["ALL_MY"] = int(float(sh.cell_value(rowx=i,colx = 1))*1e6)
				bank_data[bank_name]["ALL_FY"] = int(float(sh.cell_value(rowx=i,colx = 2))*1e6)
				bank_data[bank_name]["ALL_Y"] = int(float(sh.cell_value(rowx=i,colx = 3))*1e6)			
				rows.append([total_data[0],bank_name,"全行外匯活期存款",column[0],bank_data[bank_name]["ALL_MY"],columns_en[0]])
				rows.append([total_data[0],bank_name,"全行外匯定期存款",column[1],bank_data[bank_name]["ALL_FY"],columns_en[1]])
				#rows.append([total_data[0],bank_name,'全行外匯總存款',bank_data[bank_name]["ALL_Y"]])


			#國內總和
			if sh.cell_value(rowx=i,colx = 0)== u"總　　　　　計" and 2 == mode:
				#國內
				total_data[4] = int(float(sh.cell_value(rowx=i,colx = 1))*1e6)
				total_data[5] = int(float(sh.cell_value(rowx=i,colx = 2))*1e6)
				total_data[6] = int(float(sh.cell_value(rowx=i,colx = 3))*1e6)
				rows.append([total_data[0],"總計",'國內外匯活期存款',column[2],total_data[4],columns_en[2]])
				rows.append([total_data[0],"總計",'國內外匯定期存款',column[3],total_data[5],columns_en[3]])
				#rows.append([total_data[0],"總計",'國內外匯總存款',total_data[6]])
				#Oversea 海外
				total_data[7] = total_data[1] - total_data[4]
				total_data[8] = total_data[2] - total_data[5]
				total_data[9] = total_data[3] - total_data[6]
				rows.append([total_data[0],"總計 ",'海外外匯活期存款',column[4],total_data[7],columns_en[4]])
				rows.append([total_data[0],"總計 ",'海外外匯定期存款',column[5],total_data[8],columns_en[5]])
				#rows.append([total_data[0],"總計 ",'海外外匯總存款',total_data[9]])
				continue
			#國內銀行
			if 2 == mode:
				bank_name = unicode(sh.cell_value(rowx=i,colx = 0))
				bank_name = re.split('[\W+|(]', bank_name, flags=re.U)[0]
				bank_data[bank_name]["DB_MY"] = int(float(sh.cell_value(rowx=i,colx = 1))*1e6)
				bank_data[bank_name]["DB_FY"] = int(float(sh.cell_value(rowx=i,colx = 2))*1e6)
				bank_data[bank_name]["DB_Y"] = int(float(sh.cell_value(rowx=i,colx = 3))*1e6)
				bank_data[bank_name]["OS_MY"] = bank_data[bank_name]["ALL_MY"] - bank_data[bank_name]["DB_MY"]
				bank_data[bank_name]["OS_FY"] = bank_data[bank_name]["ALL_FY"] - bank_data[bank_name]["DB_FY"]
				bank_data[bank_name]["OS_Y"] = bank_data[bank_name]["ALL_Y"] - bank_data[bank_name]["DB_Y"]
				rows.append([total_data[0],bank_name,'國內外匯活期存款',column[2],bank_data[bank_name]["DB_MY"],columns_en[2]])
				rows.append([total_data[0],bank_name,'國內外匯定期存款',column[3],bank_data[bank_name]["DB_FY"],columns_en[3]])
				#rows.append([total_data[0],bank_name,'國內外匯總存款',bank_data[bank_name]["DB_Y"]])
				rows.append([total_data[0],bank_name,'海外外匯活期存款',column[4],bank_data[bank_name]["OS_MY"],columns_en[4]])
				rows.append([total_data[0],bank_name,'海外外匯定期存款',column[5],bank_data[bank_name]["OS_FY"],columns_en[5]])
				#rows.append([total_data[0],bank_name,'海外外匯總存款',bank_data[bank_name]["OS_Y"]])
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




 		
def parserAll():
	folder = 'Y_BAL'
	#from_path= '/Users/aha/Dropbox/Project/Financial/Plan/rawdata/%s/' % (folder)
	#to_path = '/Users/aha/Dropbox/Project/Financial/Plan/data/%s/' % (folder)
	from_path= '/home/aha/Data/TWFS/rawdata/%s/' % (folder)
	to_path = '/home/aha/Data/TWFS/data/%s/' % (folder)
	checkFolder(to_path)

	for yy in range(95,100):
		for mm in range(1,13):
			date = '%d%02d'%(yy,mm)
			parse(from_path,to_path,date)
	parse(from_path,to_path,'10001')
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
	


