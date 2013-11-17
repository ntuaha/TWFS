# -*- coding: utf-8 -*- 
import os
import sys
import psycopg2
from csv import reader

def type1(path,out_path,fn):
	pass

def run(ff):
	f = open(ff,"r")
	lines =reader(f)

	#lines = f.readlines()
	conn = psycopg2.connect(database="data", user="aha", password="dataaha305", host="localhost", port="5432")
	cur = conn.cursor()
	count = 0
	for line in lines:
		count = count +1
		if count == 1:
			continue
		

		cols = line
		Bank_Code = -1
		if cols[0] !="":
			Bank_Code = int(cols[0])
		Bank_Nm = cols[1]
		Bank_Status_Cd = "A"
		if "*" in Bank_Nm:
			Bank_Statud_Cd = "B"
		Bank_En_Name = cols[3].replace("'","''")

		Start_Ym = cols[4]
		Year = None
		Month = None
		Day = None
		if "年" in cols[4]:
			Year = cols[4].split("年")[0]
			if "月" in cols[4]:
				Month = cols[4].split("年")[1].split("月")[0]
				if "日" in cols[4]:
					Day = cols[4].split("年")[1].split("月")[1].split("日")[0]
			Start_Ym = Year
			if Month == None:
				Start_Ym = Start_Ym+"-01-01"
			else:
				Start_Ym = "%s-%s"%(Start_Ym,Month)
				if Day == None:
					Start_Ym = Start_Ym+"-01"
				else:
					Start_Ym = Start_Ym+"-"+Day
		else:
			Start_Ym = None
		Comment = cols[2]
		SWIFT_BIC = cols[5]
		if SWIFT_BIC =="無":
			SWIFT_BIC=""
		Bank_Type_Cd = cols[6]
		Bank_Area_Cd = cols[7]
		print cols[9]
		Bank_Status_Cd = cols[8]
		Current_Bank_Cd = 0
		if cols[9] != "":
			Current_Bank_Cd = int(cols[9])

		sql = "SELECT Bank_Nm,Data_Dt FROM bank_attr where Bank_Nm = '%s' order by Data_Dt desc limit 1;"%(Bank_Nm)
		#print sql
		cur.execute(sql)
		row = None
		#有資料就更新
		for row in cur.fetchall():
			if Start_Ym == None :
				sql2 = "UPDATE bank_attr SET Bank_Status_Cd = '%s',Bank_En_Nm = '%s',Comment='%s',SWIFT_BIC='%s' ,Bank_Type_Cd=%s,Bank_Area_Cd=%s,Current_Bank_Cd='%03d' where Bank_Nm='%s' and Data_Dt = '%s';"\
				%(Bank_Status_Cd,Bank_En_Name,Comment,SWIFT_BIC,Bank_Type_Cd,Bank_Area_Cd,Current_Bank_Cd,row[0],row[1])
			else:
				sql2 = "UPDATE bank_attr SET Bank_Status_Cd = '%s',Bank_En_Nm = '%s',Comment='%s',SWIFT_BIC='%s' ,Bank_Type_Cd=%s,Bank_Area_Cd=%s,Current_Bank_Cd='%03d',Start_Ym='%s' where Bank_Nm='%s' and Data_Dt = '%s';"\
				%(Bank_Status_Cd,Bank_En_Name,Comment,SWIFT_BIC,Bank_Type_Cd,Bank_Area_Cd,Current_Bank_Cd,Start_Ym,row[0],row[1])
			#print "SQL %s"%sql2
			cur.execute(sql2)
		#沒有資料就新增
		if row == None:
			if Start_Ym ==None:
				sql2 = "INSERT INTO bank_attr (Bank_Status_Cd,Bank_En_Nm,Comment,SWIFT_BIC,Bank_Type_Cd,Bank_Area_Cd,Current_Bank_Cd,Bank_Nm,Data_Dt,Bank_Code) VALUES ('%s','%s','%s','%s' ,%s,%s,'%03d','%s',Now(),'%03d');"\
				%(Bank_Status_Cd,Bank_En_Name,Comment,SWIFT_BIC,Bank_Type_Cd,Bank_Area_Cd,Current_Bank_Cd,Bank_Nm,Bank_Code)
			else:
				sql2 = "INSERT INTO bank_attr (Start_Ym,Bank_Status_Cd,Bank_En_Nm,Comment,SWIFT_BIC,Bank_Type_Cd,Bank_Area_Cd,Current_Bank_Cd,Bank_Nm,Data_Dt,Bank_Code) VALUES ('%s','%s','%s','%s','%s' ,%s,%s,'%03d','%s',Now(),'%03d');"\
				%(Start_Ym,Bank_Status_Cd,Bank_En_Name,Comment,SWIFT_BIC,Bank_Type_Cd,Bank_Area_Cd,Current_Bank_Cd,Bank_Nm,Bank_Code)
			#print sql2
			cur.execute(sql2)
		conn.commit()
	conn.close()
	f.close()
	




if __name__ == '__main__':
	run("/home/aha/Data/TWFS/data/Bank_Info/20131116/List1.csv")