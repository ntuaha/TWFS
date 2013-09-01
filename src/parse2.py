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
	print "The number of worksheets is",book.nsheets
	print "Worksheet name(s):", book.sheet_names()
	modes = [1,1,1,2,2,2]
	bank_data = {}
	header = ['年月','銀行','銀行英文','全行外匯活期存款','全行外匯定期存款','全行總額','國內外匯活期存款','國內外匯定期存款','國內總額','海外外匯活期存款','海外外匯定期存款','海外總額','金控註記']
	total_data = range(len(header)-3)
	for sheet_num in range(book.nsheets):
		sh = book.sheet_by_index(sheet_num)
		#print sh.name, sh.nrows, sh.ncols

		
		mode  = modes[sheet_num]

		for i in range(sh.nrows):
			row_name = unicode(sh.cell_value(rowx=i,colx = 0))

			#print u"2-5　一般銀行外匯存款餘額									"
			#if row_name == u"2-5　一般銀行外匯存款餘額":
			#	print "yes"
			#print "%d - %s, %s" % (i,row_name,unicode(sh.cell_value(rowx=i,colx = 1)))
			if unicode(sh.cell_value(rowx=i,colx = 1)) == u"":	
				#空的但是資料開頭就跳到資料頭		
		#		if  row_name == u"2-5　一般銀行外匯存款餘額":
		#			mode =1
				
				#if row_name == u"2-5　一般銀行外匯存款餘額（續一）":
		#			mode1_line = i+jump_gap
				
		#		if row_name== u"2-5　一般銀行外匯存款餘額（續二）":
		#			mode1_line = i+jump_gap
				
		#		if row_name == u"2-5　一般銀行外匯存款餘額（續三）":
		#			mode =2

		#		print "%d: Empty:%s" %(i,row_name)
				continue
			
			#第二藍衛如果是文字就跳過
			if len(re.findall(r"[-+]?\d*\.\d+|\d+",unicode(sh.cell_value(rowx=i,colx = 1)))) == 0:
				continue

			#全行總和
			if row_name== u"總　　　　　計" and 1 == mode:
				total_data[0] = date
				total_data[1] = float(sh.cell_value(rowx=i,colx = 1))*1e6
				total_data[2] = float(sh.cell_value(rowx=i,colx = 2))*1e6
				total_data[3] = float(sh.cell_value(rowx=i,colx = 3))*1e6
				continue
			#全行銀行
			if 1 == mode:
				bank_name = unicode(sh.cell_value(rowx=i,colx = 0))
				bank_data[bank_name] = {}
				bank_data[bank_name]["ALL_MY"] = float(sh.cell_value(rowx=i,colx = 1))*1e6
				bank_data[bank_name]["ALL_FY"] = float(sh.cell_value(rowx=i,colx = 2))*1e6
				bank_data[bank_name]["ALL_Y"] = float(sh.cell_value(rowx=i,colx = 3))*1e6


			#國內總和
			if sh.cell_value(rowx=i,colx = 0)== u"總　　　　　計" and 2 == mode:
				#國內
				total_data[4] = float(sh.cell_value(rowx=i,colx = 1))*1e6
				total_data[5] = float(sh.cell_value(rowx=i,colx = 2))*1e6
				total_data[6] = float(sh.cell_value(rowx=i,colx = 3))*1e6
				#Oversea 海外
				total_data[7] = total_data[1] - total_data[4]
				total_data[8] = total_data[2] - total_data[5]
				total_data[9] = total_data[3] - total_data[6]
				continue
			#國內銀行
			if 2 == mode:
				bank_name = unicode(sh.cell_value(rowx=i,colx = 0))
				#try:
				bank_data[bank_name]["DB_MY"] = float(sh.cell_value(rowx=i,colx = 1))*1e6
				bank_data[bank_name]["DB_FY"] = float(sh.cell_value(rowx=i,colx = 2))*1e6
				bank_data[bank_name]["DB_Y"] = float(sh.cell_value(rowx=i,colx = 3))*1e6
				bank_data[bank_name]["OS_MY"] = bank_data[bank_name]["ALL_MY"] - bank_data[bank_name]["DB_MY"]
				bank_data[bank_name]["OS_FY"] = bank_data[bank_name]["ALL_FY"] - bank_data[bank_name]["DB_FY"]
				bank_data[bank_name]["OS_Y"] = bank_data[bank_name]["ALL_Y"] - bank_data[bank_name]["DB_Y"]
				#except KeyError:
				#	print bank_name

					#print "%s %% %s" %(bank_data[bank_name],bank_name)

	output(destination_path,date,total_data,bank_data,header)
				







#輸出
def output(destination_path,date,total_data,bank_data,header):
	f = open("%sTotal.csv"%(destination_path),"a+")
	f.write(",".join(map(str,map(int,total_data)))+"\n")
	f.close()
	f = open("%s%s.csv"%(destination_path,date),"w+")
	#header = ['年月','銀行','銀行英文','全行外匯活期存款','全行外匯定期存款','全行總額','國內外匯活期存款','國內外匯定期存款','國內總額','海外外匯活期存款','海外外匯定期存款','海外總額','金控註記']
	f.write(",".join(header)+"\n")
	for i in bank_data:
		try:
			d = [None]*13
			#print "%s,%d"% (i,len(re.findall("#",i)))
			#print re.split('[\W+|(]', i, flags=re.U)[0]
			d[0] = date
			d[1] = re.split('[\W+|(]', i, flags=re.U)[0]
			d[2] = ""
			d[3] = int(bank_data[i]["ALL_MY"])
			d[4] = int(bank_data[i]["ALL_FY"])
			d[5] = int(bank_data[i]["ALL_Y"])
			d[6] = int(bank_data[i]["DB_MY"])
			d[7] = int(bank_data[i]["DB_FY"])
			d[8] = int(bank_data[i]["DB_Y"])
			d[9] = int(bank_data[i]["OS_MY"])
			d[10] = int(bank_data[i]["OS_FY"])
			d[11] = int(bank_data[i]["OS_Y"])
			d[12] = len(re.findall("#",i))
			f.write(",".join(map(str,d))+"\n")
		except KeyError:
			f.write(",".join(map(str,d))+"\n")

	f.close()


 		




if __name__ == '__main__':
	from_path= '/Users/aha/Dropbox/Project/Financial/Data/'
	to_path = '/Users/aha/Dropbox/Project/Financial/Codes/'
	cmd = "rm %sTotal.csv"%(to_path)
	os.system(cmd)

	f = open("%sTotal.csv"%(to_path),"a+")
	total_header = ['年月','全行外匯活期存款','全行外匯定期存款','全行總額','國內外匯活期存款','國內外匯定期存款','國內總額','海外外匯活期存款','海外外匯定期存款','海外總額']
	f.write(",".join(total_header)+"\n")
	f.close()
	yy = 101
	mm = 3
	#for yy in range(95,100):
#		for mm in range(1,13):
	date = '%d%02d'%(yy,mm)
	parse(from_path,to_path,date)
	#parse(from_path,to_path,'10001')


