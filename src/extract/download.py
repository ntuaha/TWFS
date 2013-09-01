# -*- coding: utf-8 -*- 

import urllib2
import urllib
import time
from datetime import date
import numpy as np
import webbrowser
import os

#下載2-5使用
def download(year,month):
	password = "aruxopq0rliabmUVxillmnWcop79abcdLXpemqeZijklqefgelfqeiIJKprlineYdeaBNyneytthjjlobc93A456hijki"
	random_number = np.random.random_integers(0,len(password)-1,8)
	pwd  = "".join([ password[i] for i in random_number])
	#server_path = "https://survey.banking.gov.tw/statis/stmain.jsp?sys=120&ym=%d%02d&ymt=%d%02d&kind=0&type=2&funid=2050&cycle=0&outmode=3&rdm=%8s" %(year,month,year,month,pwd)
	server_path = "https://survey.banking.gov.tw/statis/2_1_%d%02d%d%02d/22050.xls" % (year,month,year,month)
	client_path = "/Users/aha/Dropbox/Project/Financial/Data/%d%02d.xls" % (year,month)
	cookie_path = '/Users/aha/Dropbox/Project/Financial/Data/cookie0001.txt'
	agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31'
	print server_path
	print client_path
	cmd = 'curl -A "%s" -o %s -D %s %s'% (agent,client_path,cookie_path,server_path)
	os.system(cmd)

def getPassword():
	password = "aruxopq0rliabmUVxillmnWcop79abcdLXpemqeZijklqefgelfqeiIJKprlineYdeaBNyneytthjjlobc93A456hijki"
	random_number = np.random.random_integers(0,len(password)-1,8)
	pwd  = "".join([ password[i] for i in random_number])
	return pwd

def checkFolder(folder):
	if os.path.exists(folder) == False:
		os.mkdir(folder)


def download_2(base_path,year,month,categories_idx,filename,foldername):
	#pwd = getPassword()
	#server_path = "https://survey.banking.gov.tw/statis/stmain.jsp?sys=120&ym=%d%02d&ymt=%d%02d&kind=0&type=2&funid=2050&cycle=0&outmode=3&rdm=%8s" %(year,month,year,month,pwd)                    
	server_path = "https://survey.banking.gov.tw/statis/%s_%d%02d%d%02d/%s.xls" % (categories_idx,year,month,year,month,filename)
	client_path = "%srawdata/%s/%d%02d.xls" % (base_path,foldername,year,month)
	cookie_path = "%scookie0001.txt" % (base_path)
	agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31'
	print server_path
	print client_path
	cmd = 'curl -A "%s" -o %s -D %s %s'% (agent,client_path,cookie_path,server_path)
	os.system(cmd)	


if __name__ == '__main__':
	#設定下載起頭年份
	start_year = 95	
	end_year = 102
	base_path = "/home/aha/Data/TWFS/src/extract/" 
	#設定其它參數
	CIS = ["4_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1"]
	FOLDERS = ["DFEI","MD_BAL","MD_AUM","FD_BAL","NC","Y_BAL","CD","AREA_DP","CC","ATM","OC","PFEI"]
	#確保資料夾存在
	for fd in FOLDERS:
		checkFolder("/Users/aha/Dropbox/Project/Financial/Plan/rawdata/"+fd+"/")

	FILES = ["4140","22010","22020","22030","22040","22050","22060","213010","29010","28010","21020","21010"]
	
	#開始下載
	for year in range(start_year,end_year+1):
		for month in range(1,12):
#			download(year,month)
			for i in range(0,len(FOLDERS)):
				download_2(base_path,year,month,CIS[i],FILES[i],FOLDERS[i])

