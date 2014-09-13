# -*- coding: utf-8 -*- 

import urllib2
import urllib
import time
from datetime import date
import numpy as np
import webbrowser
import os
import sys

class DL:
	CIS = ["4_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1"]
	FOLDERS = ["DFEI","MD_BAL","MD_AUM","FD_BAL","NC","Y_BAL","CD","AREA_DP","CC","ATM","OC","PFEI"]
	FILES = ["4140","22010","22020","22030","22040","22050","22060","213010","29010","28010","21020","21010"]	
	base_path = None

	def __init__(self,base_path):
		self.base_path = base_path

	def getPassword(self):
		password = "aruxopq0rliabmUVxillmnWcop79abcdLXpemqeZijklqefgelfqeiIJKprlineYdeaBNyneytthjjlobc93A456hijki"
		random_number = np.random.random_integers(0,len(password)-1,8)
		pwd  = "".join([ password[i] for i in random_number])
		return pwd

	def checkFolder(self,folder):
		if os.path.exists(folder) == False:
			os.makedirs(folder)

	#從金管會下載資料  
	# base_path 下載要放的位置
	# year               年份
	# month              月份
	# categories_idx     分類編號(金管會給定)
	# filename           網路上檔案名稱(金管會給定)
	# foldername         存放案目錄檔案名稱(自己設定)
	# 下載後會以民國年月呈現
	def download(self,year,month):
		for fd in self.FOLDERS:
			self.checkFolder(self.base_path+"rawdata/"+fd+"/")
		for i in range(0,len(self.FOLDERS)):
			self.execute(year,month,self.CIS[i],self.FILES[i],self.FOLDERS[i])		

	def execute(self,year,month,categories_idx,filename,foldername):
		server_path = "https://survey.banking.gov.tw/statis/%s_%d%02d%d%02d/%s.xls" % (categories_idx,year,month,year,month,filename)
		client_path = "%srawdata/%s/%d%02d.xls" % (self.base_path,foldername,year,month)
		cookie_path = "%scookie0001.txt" % (self.base_path)
		agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31'
		print server_path
		print client_path
		cmd = 'curl -A "%s" -o %s -D %s %s'% (agent,client_path,cookie_path,server_path)
		os.system(cmd)
	"""驗證下載檔案"""	

	def validation(self,year,month,categories_idx,filename,foldername):
		client_path = "%srawdata/%s/%d%02d.xls" % (self.base_path,foldername,year,month)
		if os.path.isfile(client_path) and os.stat(client_path).st_size>2046:
			print "%s Done!"%(foldername)
			return True
		else:
			print "%s ERROR!!!!!!!!"%(foldername)
			return False

	#下載全部資料	
	def downloadAll(self):

		for year in range(start_year,end_year+1):
			for month in range(1,13):
				self.download(year,month)

if __name__ == '__main__':

	year= int(sys.argv[1])
	month = int(sys.argv[2])

	d =  DL('/home/aha/Data/TWFS/')
	d.download(year,month)

	
	


