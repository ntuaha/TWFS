# -*- coding: utf-8 -*- 


#PFEI
import xlrd
import re

#處理掉unicode 和 str 在ascii上的問題
import sys 
import os
reload(sys) 
sys.setdefaultencoding('utf8') 


def row1(arr,date,data):
	d = {date,"貨幣總計數",data}
	arr.append(d)
def row1(arr,date,data):
	d = {date,"貨幣總計數",data}
	arr.append(d)



def parse_1(source_path,destination_path,date):

	book = xlrd.open_workbook(source_path+date+".xls")
	#print "The number of worksheets is",book.nsheets
	#print "Worksheet name(s):", book.sheet_names()
	sh = book.sheet_by_index(0)
	#print sh.name, sh.nrows, sh.ncols
	header=['年月','項目','數值']
	country_data =[]

	row1 = {0:date,1:"MIB",2:int(float(sh.cell_value(rowx=7,colx = 1))*1e6)}
	country_data.append(row1)
	row1 = {0:date,1:"金融機構存款餘額",2:int(float(sh.cell_value(rowx=8,colx = 1))*1e6)}	
	country_data.append(row1)
	row1 = {0:date,1:"金融機構放款餘額",2:int(float(sh.cell_value(rowx=9,colx = 1))*1e6)}		
	country_data.append(row1)
	row1 = {0:date,1:"貨幣機構存款餘額",2:int(float(sh.cell_value(rowx=10,colx = 1))*1e6)}	
	country_data.append(row1)
	row1 = {0:date,1:"貨幣機構放款餘額",2:int(float(sh.cell_value(rowx=11,colx = 1))*1e6)}
	country_data.append(row1)
	row1 = {0:date,1:"一般銀行國內總分行對中小企業放款",2:int(float(sh.cell_value(rowx=12,colx = 1))*1e6)}	
	country_data.append(row1)
	row1 = {0:date,1:"一般銀行國內總分行及信用合作社消費者貸款餘額",2:int(float(sh.cell_value(rowx=13,colx = 1))*1e6)}		
	country_data.append(row1)
	row1 = {0:date,1:"一般銀行國內總分行消費者貸款餘額",2:int(float(sh.cell_value(rowx=14,colx = 1))*1e6)}			
	country_data.append(row1)
	row1 = {0:date,1:"信託基金月底餘額",2:int(float(sh.cell_value(rowx=15,colx = 1))*1e6)}				
	country_data.append(row1)
	row1 = {0:date,1:"票券公司票債券交易金額(本月)",2:int(float(sh.cell_value(rowx=16,colx = 1))*1e6)}				
	country_data.append(row1)
	row1 = {0:date,1:"票券公司票債券交易金額(本年）",2:int(float(sh.cell_value(rowx=17,colx = 1))*1e6)}	
	country_data.append(row1)
	row1 = {0:date,1:"股價指數",2:float(sh.cell_value(rowx=18,colx = 1))}	
	country_data.append(row1)
	row1 = {0:date,1:"WPI",2:float(sh.cell_value(rowx=19,colx = 1))}		
	country_data.append(row1)
	row1 = {0:date,1:"CPI",2:float(sh.cell_value(rowx=20,colx = 1))}	
	country_data.append(row1)
	row1 = {0:date,1:"匯率",2:float(sh.cell_value(rowx=21,colx = 1))}			
	country_data.append(row1)
	row1 = {0:date,1:"央行重貼現率",2:float(sh.cell_value(rowx=22,colx = 1))}
	country_data.append(row1)
	row1 = {0:date,1:"基準利率",2:float(sh.cell_value(rowx=23,colx = 1))}	
	country_data.append(row1)
	row1 = {0:date,1:"經濟成長率",2:float(sh.cell_value(rowx=36,colx = 1))}		
	country_data.append(row1)
	row1 = {0:date,1:"外匯存底",2:int(float(sh.cell_value(rowx=25,colx = 1))*1e6)}	
	country_data.append(row1)
	output(destination_path,date,country_data)
				
def parse_2(source_path,destination_path,date):

	book = xlrd.open_workbook(source_path+date+".xls")
	sh = book.sheet_by_index(0)

	header=['年月','項目','數值']
	country_data =[]

	row1 = {0:date,1:"MIB",2:int(float(sh.cell_value(rowx=7,colx = 1))*1e6)}
	country_data.append(row1)
	row2 = {0:date,1:"金融機構存款餘額",2:int(float(sh.cell_value(rowx=8,colx = 1))*1e6)}	
	country_data.append(row2)
	row3 = {0:date,1:"金融機構放款餘額",2:int(float(sh.cell_value(rowx=9,colx = 1))*1e6)}		
	country_data.append(row3)
	row4 = {0:date,1:"貨幣機構存款餘額",2:int(float(sh.cell_value(rowx=10,colx = 1))*1e6)}	
	country_data.append(row4)
	row5 = {0:date,1:"貨幣機構放款餘額",2:int(float(sh.cell_value(rowx=11,colx = 1))*1e6)}
	country_data.append(row5)
	row6 = {0:date,1:"一般銀行國內總分行對中小企業放款",2:int(float(sh.cell_value(rowx=12,colx = 1))*1e6)}	
	country_data.append(row6)
	row7 = {0:date,1:"一般銀行國內總分行及信用合作社消費者貸款餘額",2:int(float(sh.cell_value(rowx=13,colx = 1))*1e6)}		
	country_data.append(row7)
	row8 = {0:date,1:"一般銀行國內總分行消費者貸款餘額",2:int(float(sh.cell_value(rowx=14,colx = 1))*1e6)}			
	country_data.append(row8)
	row9 = {0:date,1:"票券公司票債券交易金額(本月)",2:int(float(sh.cell_value(rowx=15,colx = 1))*1e6)}				
	country_data.append(row9)
	row10 = {0:date,1:"票券公司票債券交易金額(本年）",2:int(float(sh.cell_value(rowx=16,colx = 1))*1e6)}	
	country_data.append(row10)
	row11 = {0:date,1:"股價指數",2:float(sh.cell_value(rowx=17,colx = 1))}	
	country_data.append(row11)
	row12 = {0:date,1:"WPI",2:float(sh.cell_value(rowx=18,colx = 1))}		
	country_data.append(row12)
	row13 = {0:date,1:"CPI",2:float(sh.cell_value(rowx=19,colx = 1))}	
	country_data.append(row13)
	row14 = {0:date,1:"匯率",2:float(sh.cell_value(rowx=20,colx = 1))}			
	country_data.append(row14)
	row15 = {0:date,1:"央行重貼現率",2:float(sh.cell_value(rowx=21,colx = 1))}
	country_data.append(row15)
	row16 = {0:date,1:"基準利率",2:float(sh.cell_value(rowx=22,colx = 1))}	
	country_data.append(row16)
	row17 = {0:date,1:"經濟成長率",2:float(sh.cell_value(rowx=35,colx = 1))}		
	country_data.append(row17)
	row18 = {0:date,1:"外匯存底",2:int(float(sh.cell_value(rowx=24,colx = 1))*1e6)}	
	country_data.append(row18)
	output(destination_path,date,country_data)



#輸出
def output(destination_path,date,data):
	header=['年月','項目','數值']
	f = open("%s%s.csv"%(destination_path,date),"w+")
	f.write(",".join(header)+"\n")
	for d in data:
		p=[d[i] for i in d]
		try:
			f.write(",".join(map(str,p))+"\n")
		except KeyError:
			f.write(",".join(map(str,p))+"\n")
	f.close()

def checkFolder(folder):
	if os.path.exists(folder) == False:
		os.makedirs(folder)
 		


def runAll():
	from_path= '/home/aha/Data/TWFS/rawdata/PFEI/'
	to_path = '/home/aha/Data/TWFS/data/PFEI/'
	checkFolder(to_path)
	yy = 95
	mm = 1
	for yy in range(95,97):
		for mm in range(1,13):
			parse_1(from_path,to_path,'%d%02d'%(yy,mm))
	for mm in range(1,9):
		parse_1(from_path,to_path,'%d%02d'%(97,mm))
	for mm in range(9,13):
		parse_2(from_path,to_path,'%d%02d'%(97,mm))
	for yy in range(98,103):
		for mm in range(1,13):
			parse_2(from_path,to_path,'%d%02d'%(yy,mm))


if __name__ == '__main__':
#	from_path= '/Users/aha/Dropbox/Project/Financial/Plan/rawdata/PFEI/'
#	to_path = '/Users/aha/Dropbox/Project/Financial/Plan/data/PFEI/'
#	parse_1(from_path,to_path,'9501')
#	parse_2(from_path,to_path,'10206')
	runAll()
	


