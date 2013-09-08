# -*- coding: utf-8 -*- 

import xlrd
import re

#處理掉unicode 和 str 在ascii上的問題
import sys 
import os
reload(sys) 
sys.setdefaultencoding('utf8') 

class TRANSFORM_MD_AUM:
	header=['年月','銀行','銀行類別','項目','數值']
	rows = []
	total_data = [None]*15
	bank_data = {}
	modelist = ['本國銀行','外國銀行在台分行','大陸地區銀行在臺分行']
	columns = ['活儲月平均餘額']
	source_type = 'MD_AUM' #處理活儲月均
	def __init__(self,source_path,destination_path):
		self.source_path = "%s%s/" % (source_path,self.source_type)
		self.destination_path = "%s%s/" % (destination_path,self.source_type)
		self.date = '9501'
	def clean(self):
		del self.rows[:]		

	def parse(self):
		self.clean()
		book = xlrd.open_workbook(self.source_path+self.date+".xls")
		sh = book.sheet_by_index(0)
		jump_gap = 8
		mode  = 0
		for i in range(sh.nrows):
			row_name = unicode(sh.cell_value(rowx=i,colx = 0))
						
			if u"2-2　一般銀行存款月平均餘額" in row_name:
				mode =1
#			elif u"外國銀行在臺分行小計" in row_name:
#				mode =2	
#			elif u"信用卡公司小計" in row_name:
#				mode =3			

			#空的但是資料開頭就跳到資料頭
			if unicode(sh.cell_value(rowx=i,colx = 1)) == u"":	
				continue
			#第二藍衛如果是文字就跳過
			if len(re.findall(r"[-+]?\d*\.\d+|\d+",unicode(sh.cell_value(rowx=i,colx = 1)))) != 1: #我只要一組數字的欄位
				continue

			self.total_data[0] = self.date
			self.total_data[1] = int(float(sh.cell_value(rowx=i,colx = 1))*1e6)
		
			if u"總　　　　　計" in row_name:
				for i in range(len(self.columns)):
					self.rows.append([self.date,"總計","全體本國銀行機構",self.columns[i],self.total_data[i+1]])	
			elif u"外國銀行在臺分行" in row_name:
				print True
				for i in range(len(self.columns)):
					self.rows.append([self.date,"小計",self.modelist[1],self.columns[i],self.total_data[i+1]])		
			else: #其它一般資料
				print "%s,%d" % (str(False),mode)

				bank_name = unicode(sh.cell_value(rowx=i,colx = 0))
				bank_name = re.split('[\W+|(]', bank_name, flags=re.U)[0]
				for i in range(len(self.columns)):
					self.rows.append([self.date,bank_name,self.modelist[mode-1],self.columns[i],self.total_data[i+1]])
		#將資料寫入csv
		self.output()


	def parse2(self):
		self.clean()
		book = xlrd.open_workbook(self.source_path+self.date+".xls")
		#print "The number of worksheets is",book.nsheets
		#print "Worksheet name(s):", book.sheet_names()
		bank_data = {}
		#total_data = [None]*15
		#header=['年月','銀行','項目','數值']
		#rows = []
		#total_data[0] = date
		#mode = 0
		#modelist = ['本國銀行']
		#columns = ['活儲月平均餘額']
		for sheet_num in range(book.nsheets):
			sh = book.sheet_by_index(sheet_num)
			for i in range(sh.nrows):
				row_name = unicode(sh.cell_value(rowx=i,colx = 0))
						
				if u"2-2　一般銀行存款月平均餘額" in row_name:
					mode =1
	#			elif u"外國銀行在臺分行小計" in row_name:
	#				mode =2	
	#			elif u"信用卡公司小計" in row_name:
	#				mode =3			

				#空的但是資料開頭就跳到資料頭
				if unicode(sh.cell_value(rowx=i,colx = 1)) == u"":	
					continue
				#第二藍衛如果是文字就跳過
				if len(re.findall(r"[-+]?\d*\.\d+|\d+",unicode(sh.cell_value(rowx=i,colx = 1)))) != 1: #我只要一組數字的欄位
					continue

				self.total_data[0] = self.date
				self.total_data[1] = int(float(sh.cell_value(rowx=i,colx = 1))*1e6)
			
				if u"總　　　　　計" in row_name:
					for i in range(len(self.columns)):
						self.rows.append([self.date,"總計","全體本國銀行機構",self.columns[i],self.total_data[i+1]])	
				elif u"外國銀行在臺分行" in row_name:
					print True
					for i in range(len(self.columns)):
						self.rows.append([self.date,"小計",self.modelist[1],self.columns[i],self.total_data[i+1]])		
				elif u"大陸地區銀行在臺分行" in row_name:
					print True
					for i in range(len(self.columns)):
						self.rows.append([self.date,"小計",self.modelist[2],self.columns[i],self.total_data[i+1]])	
				else: #其它一般資料
					print "%s,%d" % (str(False),mode)

					bank_name = unicode(sh.cell_value(rowx=i,colx = 0))
					bank_name = re.split('[\W+|(]', bank_name, flags=re.U)[0]
					for i in range(len(self.columns)):
						self.rows.append([self.date,bank_name,self.modelist[mode-1],self.columns[i],self.total_data[i+1]])
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
		print self.date
		
	def checkFolder(self,folder):
		if os.path.exists(folder) == False:
			os.makedirs(folder)



	def runParse(self,date):
		#from_path= '/Users/aha/Dropbox/Project/Financial/Plan/rawdata/%s/' % (source_type)
		#to_path = '/Users/aha/Dropbox/Project/Financial/Plan/data/%s/' % (source_type)
		#from_path= '/home/aha/Data/TWFS/rawdata/%s/' % (folder)
		#to_path = '/home/aha/Data/TWFS/data/%s/' % (folder)
		self.checkFolder(self.destination_path)
		self.date = date

 		self.parse2()

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
	#parserAll()
	parser = TRANSFORM_MD_AUM('/Users/aha/Dropbox/Project/Financial/Plan/rawdata/','/Users/aha/Dropbox/Project/Financial/Plan/data/')
	parser.runParse('9912')
	parser.runParse('10201')
	parser.runParse('10204')
	#parser('9912')
	#parser2('10203')
	


