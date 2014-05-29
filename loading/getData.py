# -*- coding: utf-8 -*- 

import re

#處理掉unicode 和 str 在ascii上的問題
import sys 
import os
import psycopg2

reload(sys) 
sys.setdefaultencoding('utf8') 

class GetData:
	f = None
	table = None
	col = None
	col_cal = None
	date = None
	out = None
	bank_names = ['玉山','台新','中信','國泰','花旗','富邦']
	bank_codes = ['808','812','822','013','021','012']
	def __init__(self,f,table,col_cal,col,start_dt,out):
		self.f = f
		self.table = table
		self.col = col
		self.date = start_dt
		self.out = out
		self.col_cal = col_cal
	def write(self):
		f = open(self.f,'w+')
		#

		i = 0
		#f.write("drop table G;\n")
		for code in self.bank_codes:
			#f.write("drop table A%02d;\n"%(i))
			f.write("create  temporary table A%02d as select to_char(Data_dt,'YYYY-MM-DD') as Data_dt, %s as %s from %s where bank_code = '%s' and Data_dt >= '%s' order by data_dt;\n"%(i,self.col_cal,self.col,self.table,code,self.date))
			i= i+1	
		f.write("create temporary table G as select A00.Data_dt")
		i = 0
		for code in self.bank_codes:
			f.write(",A%02d.%s as A%02d"%(i,self.col,i))
			i = i+1
		f.write("\nfrom A00")		

		for i in xrange(1,len(self.bank_codes)):
			f.write("\nleft join A%02d on (A00.data_dt = A%02d.data_dt)"%(i,i))
		f.write("\norder by data_dt;")
		f.write("\n\copy (select * from G) to '/home/aha/Data/TWFS/data/%s_2' With CSV HEADER"%self.out)
		f.close()

	def run(self):
		os.system('psql -d data -f %s'%(self.f))

	def modify(self):
		bank_names = "date,"+u",".join(self.bank_names)
		f = open("/home/aha/Data/TWFS/data/%s_2"%self.out,'r')
		f2 = open("/home/aha/Data/TWFS/data/%s"%self.out,'w+')
		lines  = f.readlines()
		i = 0
		for line in lines:
			if i==0:
				f2.write("%s\n"%bank_names)	
			else:
				f2.write(line)
			i=i+1
		f.close()
		f2.close()
		os.system("rm /home/aha/Data/TWFS/data/%s_2"%self.out)



if __name__ == "__main__":
	#worker = GetData("./getData.sql","cc","Cc_Txn_Bal","Cc_Txn_Bal",'2010-04-01','cc_txn_bal.csv')
	worker = GetData("./getData.sql",sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
	worker.write()
	worker.run()
	worker.modify()