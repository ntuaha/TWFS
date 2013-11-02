# -*- coding: utf-8 -*- 

import urllib2
import urllib
import time
from datetime import date
import numpy as np
import webbrowser
import os
import sys
from bs4 import BeautifulSoup
import psycopg2

reload(sys)
sys.setdefaultencoding('utf8')

def getPassword():
	password = "aruxopq0rliabmUVxillmnWcop79abcdLXpemqeZijklqefgelfqeiIJKprlineYdeaBNyneytthjjlobc93A456hijki"
	random_number = np.random.random_integers(0,len(password)-1,8)
	pwd  = "".join([ password[i] for i in random_number])
	return pwd

def checkFolder(folder):
	if os.path.exists(folder) == False:
		os.makedirs(folder)

def download(base_path):
	#http://www.fisc.com.tw/tc/business/Detail.aspx?caid=b38613b7-e55d-4841-bba7-25643821fe1f
	#ATM 業務
	server_path = "http://www.fisc.com.tw/tc/business/Detail.aspx?caid=b38613b7-e55d-4841-bba7-25643821fe1f"
	response = urllib2.urlopen(server_path).read()  
	#print response
	sp = BeautifulSoup(response)
	conn = psycopg2.connect(database="data", user="aha", password="dataaha305", host="localhost", port="5432")
	cur = conn.cursor()	
	
	td = sp.select("tr.bg_01 > td")
	getInfoFromTd(cur,td)
	td = sp.select("tr.bg_02 > td")
	getInfoFromTd(cur,td)
	conn.commit()
	conn.close()


def getInfoFromTd(cur,td):
	L = len(td)
	
	for i in range(L):
		if i%2 == 0:
			bank_code = td[i].string.strip().replace("\n", "")
		elif i%2 == 1 :
			bank_nm = td[i].string.strip().replace("\n", "")
			if len(bank_nm)>0:
			#bank_nm進來的時候已經是unicode
				sql = u"INSERT INTO bank_attr (bank_nm,bank_code,Data_dt) VALUES ('%s','%s',date_trunc('day',NOW()))" %(bank_nm,bank_code)
				sql = sql.encode('utf-8')
				cur.execute(sql)
				bank_code = None
				bank_nm = None

#下載全部資料	
def downloadAll():
	base_path = "/home/aha/Data/TWFS/rawdata/bank_attr/" 
	#確保資料夾存在
	checkFolder(base_path)
	download(base_path)

if __name__ == '__main__':
	downloadAll()
	


