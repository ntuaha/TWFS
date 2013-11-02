# -*- coding: utf-8 -*- 
import os
import sys


def convert(path,out_path,fn):
	f = open(path+fn,'r')
	fwname = "-".join(fn.split("-")[1:3])
	fw = open(out_path+fwname+".csv","w+")
	count = int(fn.split("-")[3].split('.')[0])	
	header = ["TEST","BIN","CONTA","CONTC","POLAR","VF1","VF2","VF3","VF4","VFM1","VFM2","DVF","VF","VFD","VZ1","VZ2","IR","LOP1","LOP2","LOP3","WLP1","WLD1","WLC1","HW1","PURITY1","X1","Y1","Z1","CCT1","ST1","INT1","WLP2","WLD2","WLC2","HW2","PURITY2","X2","Y2","Z2","CCT2","ST2","INT2","WLP3","WLD3","WLC3","HW3","PURITY3","X3","Y3","Z3","CCT3","ST3","INT3","PosX","PosY"]
	h_cnt = len(header)
	mode = 1
	row_cnt = 0		
	for line in f.readlines():
		row_cnt = row_cnt+1
		row = line.split(',')
		if mode == 1:
			if row_cnt==2:
				fw.write(fwname+",,\n")
			elif row[0] !="TEST":
				fw.write(line.strip()+"\n")
			else:
				mode =2
				fw.write(",".join(header)+"\n")
		elif mode==2:

			cols = [""]*h_cnt
			for i in xrange(0,len(row)):
				cols[i] = row[i].strip()
			cols[5] = row[3]
			cols[3] = ""
			cols[16] = row[8]
			cols[8] = ""
			cols[17] = row[28]
			cols[28] = ""
			cols[21] = row[20]
			cols[20] = row[19]
			cols[19] = ""
			cols[54] = row[27]
			cols[53] = row[26]
			cols[27] = ""
			cols[26] = ""
			fw.write(",".join(cols)+"\n")
	fw.close()
	f.close()

def extractBank(f):
	fp = open(f,'r+')
	bank_idx = -1
	bank_category_idx = -1
	lines = f.readlines()
	row = 0
	for line in lines:
		row = row+1
		cols = line.split(',')
		if row ==1:
			for i in xrange(len(cols)):
				if cols[i] == "銀行":
					bank_idx = i
				if cols[i] == "銀行分類":
					bank_category_idx = i
		else:
			if cols[bank_idx] == "總計":
				continue
			else:
				Bank_Nm = cols[bank_idx]
				Bank_En_Nm	="NULL"
				if cols[bank_category_idx] =="本國銀行":
					Bank_Area = '0'
					Bank_Categories_1 = '1'
					Bank_Categories_2 = 'NULL'
				elif cols[bank_category_idx] =="外國銀行在檯分行":
					Bank_Area = '1'
					Bank_Categories_1 = '1'
					Bank_Categories_2 = '2'
				Bank_Short_Nm = Bank_Nm[0:3]
			conn = psycopg2.connect(database="data", user="aha", password="dataaha305", host="127.0.0.1", port="5432")
			cur = conn.cursor()	
			sql = "SELECT FROM bank_attr WHERE bank_short_nm = '%s' order by Data_Ym desc limit 1;"%(Bank_Short_Nm)
			cur.execute(sql)
			rows = cur.fetchall()
			if len(rows)==0 :
				sql = "INSERT INTO bank_attr (Data_Ym) VALUES ('')"

	#ds = conn.query("DELETE FROM PFEI WHERE Data_Ym='%s'"%(date))
	cur.execute("DELETE FROM PFEI WHERE Data_Ym='%s'"%(date))
	sql = "INSERT INTO PFEI (Data_Ym,%s) VALUES (Timestamp '%s',%s)" %(cols,date,values)
	#print sql
	#conn.query(sql)
	cur.execute(sql)
	conn.commit()
	cur.execute("SELECT * FROM PFEI")
	rows = cur.fetchall()







if __name__ == '__main__':
	checkFolder = ['NC/']
	path = sys.argv[1]
	for folder in checkFolder:
		flist = os.listdir(path+folder)
		for f in flist:
			if f != '.' and f!="..":
				extractBank(path+folder+f)