# -*- coding: utf-8 -*- 

import re

#處理掉unicode 和 str 在ascii上的問題
import sys 
import os
#import pg
#import DB_INFO
reload(sys) 
sys.setdefaultencoding('utf8') 

				
def insert(table,data):

	#print DB_INFO.database
	#conn = pg.connect(DB_INFO.database,DB_INFO.server_site,DB_INFO.port,None,None,DB_INFO.username,DB_INFO.password)
	#ds = conn.query("select * from table1")
	#conn.disconnect()
	print data

def makeSQL(data):
	#reference['資料年月']='Data_Ym'
	reference={}
	#reference['PFEI資料年月']='PFEI_Data_Ym'
	reference['MIB']='M1B'
	reference['金融機構存款餘額']='F_Ins_Dp'
	reference['金融機構放款餘額']='F_Ins_Ln'
	reference['貨幣機構存款餘額']='C_Ins_Dp'
	reference['貨幣機構放款餘額']='C_Ins_Ln'
	reference['一般銀行國內總分行對中小企業放款']='Country_SME'
	reference['一般銀行國內總分行及信用合作社消費者貸款餘額']='Country_C_CL'
	reference['一般銀行國內總分行消費者貸款餘額']='Country_CL'
	reference['信託機構基金月底餘額']='MF_Bal'
	reference['票券公司票債券交易金額']='Bund_Txn_Amt'
	reference['股價指數']='Stock_Index'
	reference['WPI']='WPI'
	reference['CPI']='CPI'
	reference['美元匯率']='Exchange_Rate'
	reference['央行重貼現率']='Rediscount_Rate'
	reference['基準利率']='B_Ins_Rate'
	reference['經濟成長率']='GDP'
	reference['外匯存底']='Y_DP'
	li = [data[index] for index in reference]
	cols  = ','.join(reference)
	values = ','.join(li)
	sql = "INSERT INTO PEFI (PFEI_Data_Ym,%s) VALUES (Timestamp '%s',%s)" %(cols,data["date"],values)
	print sql




def read(source_path):
	f = open(source_path,"r")
	header = f.readline()
	data = {}
	date = None
	while 1:
		lines = f.readlines(10000)
		if not lines:
			break		
		for line in lines:
			row = line.split(',')
			year = int(row[0][0:3])+1911
			month = int(row[0][3:5])
			date = "%d-%d-01" % (year,month)
			data[row[1]] = row[2]
		data["date"] = date
	f.close()
	#insert(None,data)
	makeSQL(data)





 		




if __name__ == '__main__':
	path = '/Users/aha/Dropbox/Project/Financial/Plan/data/PESI/'
	read("%s%d.csv"%(path,10206))

