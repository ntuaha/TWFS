# -*- coding: utf-8 -*- 

import re

#處理掉unicode 和 str 在ascii上的問題
import sys 
import os
import psycopg2

reload(sys) 
sys.setdefaultencoding('utf8') 


def makeSQL(date,data,Dataset):
	bank_nms = data.keys()
	conn = psycopg2.connect(database="data", user="aha", password="dataaha305", host="127.0.0.1", port="5432")
	cur = conn.cursor()	
	bank_code = None
	add_file = open("./add_file.log","a+")
	for bank_nm in bank_nms:		

#根據銀行名稱，給定銀行代碼Bank_Code
		if bank_nm=="總計":
			bank_code = "0"	
		elif bank_nm=="本國銀行小計":
			continue
		elif bank_nm=="外國銀行在臺分行小計":
			continue
		elif bank_nm=="信用卡公司小計":
			continue
#		elif bank_nm=="小計":
#			continue				
		else:		
			sql = "SELECT bank_code FROM bank_attr WHERE bank_nm like '%%%s%%' ORDER BY Data_dt desc LIMIT 1;"%(bank_nm)
			r = cur.execute(sql)
			row = None
			for row in cur.fetchall():  				
				bank_code = row[0].strip().replace("\n","")
			if row == None:
				sql = "SELECT DISTINCT bank_code as NS FROM bank_attr WHERE bank_code like'N%' ORDER BY bank_code desc LIMIT 1;"				
				cur.execute(sql)
				bank_code = None
				for row2 in cur.fetchall():
					bank_code = "N%03d"%(int(row2[0].strip().replace("\n","")[1:])+1)
				if bank_code ==None:
					bank_code="N000"
				sql = "INSERT INTO bank_attr (bank_nm,bank_code,Data_dt) VALUES ('%s','%s',date_trunc('day',NOW()));"%(bank_nm,bank_code)
				add_file.write("%s:%s\n"%(bank_nm,sql))
				cur.execute(sql)
				conn.commit()

		data[bank_nm]["bank_code"] = "'"+bank_code+"'"
		data[bank_nm]["bank_nm"] = "'"+bank_nm+"'"
		cols  = ','.join(data[bank_nm].keys())
		li = [data[bank_nm][x] for x in data[bank_nm]]
		values = ','.join(li)
		conn.commit()
	#	print "%s:%s:%s:%s"%(date,bank_code,bank_nm,data[bank_nm]["MARKET_RATE"])
		cur.execute("DELETE FROM %s WHERE Data_dt='%s' and bank_code='%s';"%(Dataset,date,bank_code))
		sql = "INSERT INTO %s (Data_Dt,%s) VALUES (Timestamp '%s',%s);"%(Dataset,cols,date,values)
		#conn.query(sql)
		cur.execute(sql)
		conn.commit()
	
    
	add_file.close()
	conn.close()

def read(source_path,dataset):
	f = open(source_path,"r")
	header = f.readline()
	data = {}
	date = None
	while 1:
		lines = f.readlines()
		if not lines:
			break		
		for line in lines:
			rows = line.split(',')
			#去掉特殊字元
			row = [x.strip().strip("\t").strip("\r").strip("　") for x in rows]
			#確認使用
#			for i in row:
#				print i
			year = int(row[0][:-2])+1911
			month = int(row[0][-2:])
			date = "%d-%d-01" % (year,month)
			#1:中文名稱 5:英文名稱
			#if row[1]=="小計":
			#	row[1] = "外國銀行在台分行"
			if data.get(row[1],None) == None:
				data[row[1]] = {}
			if data[row[1]].get(row[5].strip().replace("\n",""),None)== None:
				data[row[1]][row[5].strip().replace("\n","")] = float(row[4])
			else:
				data[row[1]][row[5].strip().replace("\n","")] = data[row[1]][row[5].strip().replace("\n","")]+float(row[4])
	f.close()
	#print data
	for i in data:
		for j in data[i]:
			data[i][j] = str(data[i][j])
	makeSQL(date,data,dataset)

def runAll(path,t):
#	for yy in range(101,102):
#		for mm in range(1,2):
	for yy in range(95,103):
		for mm in range(1,13):
			read("%s%d%02d.csv"%(path,yy,mm),t)

if __name__ == '__main__':
	t = "CC"
	path = '/home/aha/Data/TWFS/data/%s/'%(t)
	runAll(path,t)

