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
			Bank_Nm = Bank_Nm.split("*")[1]
		Comment = cols[2]
		Bank_Type_Cd = cols[4]
		Bank_Area_Cd = 0
		Current_Bank_Cd = 0

		sql = "SELECT Bank_Nm,Data_Dt FROM bank_attr where Bank_Nm = '%s' order by Data_Dt desc limit 1;"%(Bank_Nm)
		#print sql
		cur.execute(sql)
		row = None
		#有資料就更新
		for row in cur.fetchall():
			sql2 = "UPDATE bank_attr SET Bank_Status_Cd = '%s',Comment='%s',Bank_Type_Cd=%s,Bank_Area_Cd=%s,Current_Bank_Cd='%03d' where Bank_Nm='%s' and Data_Dt = now();"\
				%(Bank_Status_Cd,Comment,Bank_Type_Cd,Bank_Area_Cd,Current_Bank_Cd,row[1])
		
			#print "SQL %s"%sql2
			cur.execute(sql2)
		#沒有資料就新增
		if row == None:

			sql2 = "INSERT INTO bank_attr (Bank_Status_Cd,Comment,Bank_Type_Cd,Bank_Area_Cd,Current_Bank_Cd,Bank_Nm,Data_Dt,Bank_Code) VALUES ('%s','%s',%s,%s,'%03d','%s',Now(),'%03d');"\
				%(Bank_Status_Cd,Comment,Bank_Type_Cd,Bank_Area_Cd,Current_Bank_Cd,Bank_Nm,Bank_Code)

			#print sql2
			cur.execute(sql2)
		conn.commit()
	conn.close()
	f.close()
	




if __name__ == '__main__':
	run("/home/aha/Data/TWFS/data/Bank_Info/20131116/List2.csv")