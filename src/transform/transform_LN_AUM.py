# -*- coding: utf-8 -*- 

import xlrd
import re

#處理掉unicode 和 str 在ascii上的問題
import sys 
import os
reload(sys) 
sys.setdefaultencoding('utf8') 

class TRANSFORM_LN_AUM:
	source_type = 'LN_AUM' 
	header=['年月','銀行','銀行類別','項目','數值','英文項目']
	rows = []
	total_data = [None]*15
	bank_data = {}
	modelist = ['本國銀行','外國銀行在台分行','大陸地區銀行在臺分行','信用合作社']
	columns = ["月均餘額"]	
	columns_en = ["LN_Aum"]	
	def __init__(self,source_path,destination_path):
		self.source_path = "%s%s/" % (source_path,self.source_type)
		self.destination_path = "%s%s/" % (destination_path,self.source_type)
		self.date = '9501'
	def clean(self):
		del self.rows[:]		

	def parse(self):
		self.clean()
		book = xlrd.open_workbook(self.source_path+self.date+".xls")
		#print "The number of worksheets is",book.nsheets
		#print "Worksheet name(s):", book.sheet_names()
		bank_data = {}
		mode = 0
		for sheet_num in range(book.nsheets):
			sh = book.sheet_by_index(sheet_num)
			for i in range(sh.nrows):
				row_name = unicode(sh.cell_value(rowx=i,colx = 0))					
				#if u"本國銀行" in row_name:					
				#	mode = 0
				#	continue													
				#if u"外國銀行在臺分行" in row_name:
				#	mode = 1
				#	continue					
				#if u"信合社及農漁會小計" in row_name:
				#	mode = 3
				#	continue									

				#空的但是資料開頭就跳到資料頭
				if unicode(sh.cell_value(rowx=i,colx = 1)) == u"":	
					continue
				#第二藍衛如果是文字就跳過
				if len(re.findall(r"[-+]?\d*\.\d+|\d+",unicode(sh.cell_value(rowx=i,colx = 1)))) != 1: #我只要一組數字的欄位
					continue
				if u"月底" in unicode(sh.cell_value(rowx=i,colx = 1)):	
					continue
				if u"End" in unicode(sh.cell_value(rowx=i,colx = 1)):	
					continue


				self.total_data[0] = self.date 
				self.total_data[1] = int(float(sh.cell_value(rowx=i,colx = 1))*1e6)

				

			
			
				#if u"總　　　　　計　Total" in row_name:
				#	for i in range(len(self.columns)):
				#		self.rows.append([self.date,"總計","全體銀行機構",self.columns[i],self.total_data[i+1]])	
				if u"總" in row_name and u"計" in row_name:
					for i in range(len(self.columns)):
						self.rows.append([self.date,"總計",self.modelist[mode],self.columns[i],self.total_data[i+1],self.columns_en[i]])							
				#elif u"本國銀行" in row_name:					
				#	for i in range(len(self.columns)):
				#		self.rows.append([self.date,"小計",self.modelist[0],self.columns[i],self.total_data[i+1]])							
				#elif u"外國銀行在臺分行" in row_name:					
				#	for i in range(len(self.columns)):
				#		self.rows.append([self.date,"小計",self.modelist[1],self.columns[i],self.total_data[i+1]])		
				#elif u"信用合作社" in row_name:
				#	for i in range(len(self.columns)):
				#		self.rows.append([self.date,"小計",self.modelist[3],self.columns[i],self.total_data[i+1]])	
				else: #其它一般資料				
					bank_name = unicode(sh.cell_value(rowx=i,colx = 0))
					#如果名稱前面有個空白就選後面那一個
					if re.split('[\W+|(]', bank_name, flags=re.U)[0] == u"" :
						bank_name = re.split('[\W+|(]', bank_name, flags=re.U)[1]
					else:
						bank_name = re.split('[\W+|(]', bank_name, flags=re.U)[0]
					for i in range(len(self.columns)):
						self.rows.append([self.date,bank_name,self.modelist[mode],self.columns[i],self.total_data[i+1],self.columns_en[i]])
		#將資料寫入csv
		self.output()
					


	#輸出
	def output(self):
		f = open("%s%s.csv"%(self.destination_path,self.date),"w+")
		f.write(",".join(self.header)+"\n")
		for d in self.rows:
			try:
				f.write(",".join(map(str,d))+"\n")
			except KeyError:
				f.write(",".join(map(str,d))+"\n")
		f.close()
		print "%s is completed!" % (self.date)
		
	def checkFolder(self,folder):
		if os.path.exists(folder) == False:
			os.makedirs(folder)

	def runParse(self,date):
		self.checkFolder(self.destination_path)
		self.date = date
 		self.parse()

	def parseAll(self):
		for yy in range(95,103):
			for mm in range(1,13):
				self.runParse('%d%02d'%(yy,mm))



if __name__ == '__main__':
#	parser = TRANSFORM_LN_AUM('/Users/aha/Dropbox/Project/Financial/Plan/rawdata/','/Users/aha/Dropbox/Project/Financial/Plan/data/')
#	parser.runParse('10001')
#	parser.runParse('10002')
	parser = TRANSFORM_LN_AUM('/home/aha/Data/TWFS/rawdata/','/home/aha/Data/TWFS/data/')
	parser.parseAll()

	


