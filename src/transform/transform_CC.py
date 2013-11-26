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
	header=['年月','銀行','銀行類別','項目','數值','英文欄位']
	rows = []
	total_data = [None]*15
	jump_gap = 8
	mode  = 0
	modelist = ['本國銀行','外國銀行在台分行','信用卡公司']
	columns = ['流通卡數','有效卡數','本月發卡數','本月停卡數','循環信用餘額','本月簽帳金額','本月預借現金金額'
	,'預期帳款比率','底被呆帳提足率','本月轉銷呆帳金額','循環信用利息收入','簽帳手續費收入','預借現金手續費','收單特約商店家數']
	columns_en = [
'Cc_F_Card_Cnt',
'Cc_Open_Card_Cnt',
'Cc_Issue_Card_Cnt',
'Cc_Stop_Card_Cnt',
'Cyc_Bal',
'Cc_Txn_Bal',
'Cc_Ln_Bal',
'Cc_Payment_Rate',
'Cc_BadDebit_Rate',
'Cc_BadDebit_Bal',
'Cyc_Income',
'Txn_Fee',
'Cc_Ln_Fee',
'Auth_Store_Cnt']


	for i in range(sh.nrows):
		row_name = unicode(sh.cell_value(rowx=i,colx = 0))
		#空的但是資料開頭就跳到資料頭
		if unicode(sh.cell_value(rowx=i,colx = 1)) == u"":	
			continue
					
		if u"本國銀行小計" in row_name:
			mode =1
		elif u"外國銀行在臺分行小計" in row_name:
			mode =2	
		elif u"信用卡公司小計" in row_name:
			mode =3

		
		#第二藍衛如果是文字就跳過
		if len(re.findall(r"[-+]?\d*\.\d+|\d+",unicode(sh.cell_value(rowx=i,colx = 1)))) == 0:
			continue
		total_data[0] = date
		total_data[1] = int(float(sh.cell_value(rowx=i,colx = 1)))
		total_data[2] = int(float(sh.cell_value(rowx=i,colx = 2)))
		total_data[3] = int(float(sh.cell_value(rowx=i,colx = 3)))
		total_data[4] = int(float(sh.cell_value(rowx=i,colx = 4)))
		total_data[5] = int(float(sh.cell_value(rowx=i,colx = 5))*1e6)
		total_data[6] = int(float(sh.cell_value(rowx=i,colx = 6))*1e6)
		total_data[7] = int(float(sh.cell_value(rowx=i,colx = 7))*1e6)
		total_data[8] = float(sh.cell_value(rowx=i,colx = 8))
		total_data[9] = float(sh.cell_value(rowx=i,colx = 9))
		total_data[10] = int(float(sh.cell_value(rowx=i,colx = 10))*1e6)
		total_data[11] = int(float(sh.cell_value(rowx=i,colx = 11))*1e6)
		total_data[12] = int(float(sh.cell_value(rowx=i,colx = 12))*1e6)
		total_data[13] = int(float(sh.cell_value(rowx=i,colx = 13))*1e6)
		total_data[14] = int(float(sh.cell_value(rowx=i,colx = 14)))
	
		if u"總　　　　計　Total" in row_name:
			for i in range(len(columns)):
				rows.append([total_data[0],"總計","全部信用卡機構",columns[i],total_data[i+1],columns_en[i]])
		elif  u"小計" in row_name:
			for i in range(len(columns)):
				rows.append([total_data[0],"小計",modelist[mode-1],columns[i],total_data[i+1],columns_en[i]])			
		else: #其它一般資料
			bank_name = unicode(sh.cell_value(rowx=i,colx = 0))
			bank_name = re.split('[\W+|(]', bank_name, flags=re.U)[0]
			for i in range(len(columns)):
				rows.append([total_data[0],bank_name,modelist[mode-1],columns[i],total_data[i+1],columns_en[i]])
	#將資料寫入csv
	output(destination_path,header,date,rows)


def parse2(source_path,destination_path,date):
	book = xlrd.open_workbook(source_path+date+".xls")
	#print "The number of worksheets is",book.nsheets
	#print "Worksheet name(s):", book.sheet_names()
	bank_data = {}
	total_data = [None]*15
	#header=['年月','銀行','項目','數值','英文欄位']
	header=['年月','銀行','銀行類別','項目','數值','英文欄位']
	rows = []
	total_data[0] = date
	mode = 0
	modelist = ['本國銀行','外國銀行在台分行','信用卡公司']
	columns = ['流通卡數','有效卡數','本月發卡數','本月停卡數','循環信用餘額','本月簽帳金額','本月預借現金金額'
	,'預期帳款比率','底被呆帳提足率','本月轉銷呆帳金額','循環信用利息收入','簽帳手續費收入','預借現金手續費','收單特約商店家數']

	columns_en = [
'Cc_F_Card_Cnt',
'Cc_Open_Card_Cnt',
'Cc_Issue_Card_Cnt',
'Cc_Stop_Card_Cnt',
'Cyc_Bal',
'Cc_Txn_Bal',
'Cc_Ln_Bal',
'Cc_Payment_Rate',
'Cc_BadDebit_Rate',
'Cc_BadDebit_Bal',
'Cyc_Income',
'Txn_Fee',
'Cc_Ln_Fee',
'Auth_Store_Cnt']
	for sheet_num in range(book.nsheets):
		sh = book.sheet_by_index(sheet_num)
		for i in range(sh.nrows):
			row_name = unicode(sh.cell_value(rowx=i,colx = 0))
			if unicode(sh.cell_value(rowx=i,colx = 1)) == u"":	
				continue
			
			#第二藍衛如果是文字就跳過
			if len(re.findall(r"[-+]?\d*\.\d+|\d+",unicode(sh.cell_value(rowx=i,colx = 1)))) == 0:
				continue
			if u"本國銀行小計" in row_name:
				mode =1
			elif u"外國銀行在臺分行小計" in row_name:
				mode =2	
			elif u"信用卡公司小計" in row_name:
				mode =3

			total_data[0] = date
			total_data[1] = int(float(sh.cell_value(rowx=i,colx = 1)))
			total_data[2] = int(float(sh.cell_value(rowx=i,colx = 2)))
			total_data[3] = int(float(sh.cell_value(rowx=i,colx = 3)))
			total_data[4] = int(float(sh.cell_value(rowx=i,colx = 4)))
			total_data[5] = int(float(sh.cell_value(rowx=i,colx = 5))*1e6)
			total_data[6] = int(float(sh.cell_value(rowx=i,colx = 6))*1e6)
			total_data[7] = int(float(sh.cell_value(rowx=i,colx = 7))*1e6)
			total_data[8] = float(sh.cell_value(rowx=i,colx = 8))
			total_data[9] = float(sh.cell_value(rowx=i,colx = 9))
			total_data[10] = int(float(sh.cell_value(rowx=i,colx = 10))*1e6)
			total_data[11] = int(float(sh.cell_value(rowx=i,colx = 11))*1e6)
			total_data[12] = int(float(sh.cell_value(rowx=i,colx = 12))*1e6)
			total_data[13] = int(float(sh.cell_value(rowx=i,colx = 13))*1e6)
			total_data[14] = int(float(sh.cell_value(rowx=i,colx = 14)))



			if u"總　　　　計" in row_name:
				for i in range(len(columns)):
					rows.append([total_data[0],"總計","全部信用卡機構",columns[i],total_data[i+1],columns_en[i]])
			elif  u"小計" in row_name:
				for i in range(len(columns)):
					rows.append([total_data[0],"小計",modelist[mode-1],columns[i],total_data[i+1],columns_en[i]])			
			else: #其它一般資料
				bank_name = unicode(sh.cell_value(rowx=i,colx = 0))
				for i in range(len(columns)):
					rows.append([total_data[0],bank_name,modelist[mode-1],columns[i],total_data[i+1],columns_en[i]])
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
	folder = 'CC'
	from_path= '/Users/aha/Dropbox/Project/Financial/Plan/rawdata/%s/' % (folder)
	to_path = '/Users/aha/Dropbox/Project/Financial/Plan/data/%s/' % (folder)
	#from_path= '/home/aha/Data/TWFS/rawdata/%s/' % (folder)
	#to_path = '/home/aha/Data/TWFS/data/%s/' % (folder)
	checkFolder(to_path)
 	parse(from_path,to_path,date)

def parser2(date):
	folder = 'CC'
	from_path= '/Users/aha/Dropbox/Project/Financial/Plan/rawdata/%s/' % (folder)
	to_path = '/Users/aha/Dropbox/Project/Financial/Plan/data/%s/' % (folder)
	#from_path= '/home/aha/Data/TWFS/rawdata/%s/' % (folder)
	#to_path = '/home/aha/Data/TWFS/data/%s/' % (folder)
	checkFolder(to_path)
 	parse2(from_path,to_path,date)

def parserAll():
	folder = 'CC'
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
	#parser('9910')
	#parser2('10203')
	


