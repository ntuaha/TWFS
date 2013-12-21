# -*- coding: utf-8 -*- 
import os
import sys
reload(sys) 
sys.setdefaultencoding('utf8')
def extract(year,month):
	from extract.download import Download
	base_path = "/home/aha/Data/TWFS/" 
	#設定其它參數
	CIS = ["4_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1"]
	FOLDERS = ["DFEI","MD_BAL","MD_AUM","FD_BAL","NC","Y_BAL","CD","AREA_DP","CC","ATM","OC","PFEI","LPPE","LSME","LN","LN_AUM","CL","CL_INFO"]
	FILES = ["4140","22010","22020","22030","22040","22050","22060","213010","29010","28010","21020","21010","24030","24040","24010","24020","25010","25020"]	
	dlAgent = Download()
	for fd in FOLDERS:
		dlAgent.checkFolder(base_path+"rawdata/"+fd+"/")

	for i in range(0,len(FOLDERS)):
		dlAgent.download(base_path,year,month,CIS[i],FILES[i],FOLDERS[i])
	isResult = True
	for i in range(0,len(FOLDERS)):
		#這兩個目前有問題跳過
		if FOLDERS[i] == "OC" or FOLDERS[i]=="AREA_DP":
			continue
		isResult = isResult and dlAgent.validation(base_path,year,month,CIS[i],FILES[i],FOLDERS[i])
	return isResult

def checkFolder(folder):
	if os.path.exists(folder) == False:
		os.makedirs(folder)

def validation(path):
	if os.path.isfile(path) and os.stat(path).st_size>500:
		print "%s Done!"%(path)
		return True
	else:
		print "%s ERROR!!!!!!!!"%(path)
		return False

def transform(year,month):
	def run(folder,transformFunction,year,month):
		from_path= '/home/aha/Data/TWFS/rawdata/%s/' % (folder)
		to_path = '/home/aha/Data/TWFS/data/%s/' % (folder)
		checkFolder(to_path)
		date = '%d%02d'%(year,month)
		#Transform_Y_Bal
		transformFunction(from_path,to_path,date)	
	import transform.transform_Y_Bal
	run("Y_BAL",transform.transform_Y_Bal.parse2,year,month)
	import transform.transform_ATM
	parser = transform.transform_ATM.TRANSFORM_ATM('/home/aha/Data/TWFS/rawdata/','/home/aha/Data/TWFS/data/')
	parser.runParse('%d%02d'%(year,month))
	import transform.transform_CC
	run("CC",transform.transform_CC.parse2,year,month)
	import transform.transform_CD
	parser = transform.transform_CD.TRANSFORM_CD('/home/aha/Data/TWFS/rawdata/','/home/aha/Data/TWFS/data/')
	parser.runParse('%d%02d'%(year,month))
	import transform.transform_CL_INFO
	parser = transform.transform_CL_INFO.TRANSFORM_CL_INFO('/home/aha/Data/TWFS/rawdata/','/home/aha/Data/TWFS/data/')
	parser.runParse('%d%02d'%(year,month))
	import transform.transform_CL	
	parser = transform.transform_CL.TRANSFORM_CL('/home/aha/Data/TWFS/rawdata/','/home/aha/Data/TWFS/data/')
	parser.runParse('%d%02d'%(year,month))
	import transform.transform_FD_BAL	
	parser = transform.transform_FD_BAL.TRANSFORM_FD_BAL('/home/aha/Data/TWFS/rawdata/','/home/aha/Data/TWFS/data/')
	parser.runParse('%d%02d'%(year,month))
	import transform.transform_LN_AUM
	parser = transform.transform_LN_AUM.TRANSFORM_LN_AUM('/home/aha/Data/TWFS/rawdata/','/home/aha/Data/TWFS/data/')
	parser.runParse('%d%02d'%(year,month))
	import transform.transform_LN
	parser = transform.transform_LN.TRANSFORM_LN('/home/aha/Data/TWFS/rawdata/','/home/aha/Data/TWFS/data/')
	parser.runParse('%d%02d'%(year,month))
	import transform.transform_LPPE
	parser = transform.transform_LPPE.TRANSFORM_LPPE('/home/aha/Data/TWFS/rawdata/','/home/aha/Data/TWFS/data/')
	parser.runParse('%d%02d'%(year,month))
	import transform.transform_LSME
	parser = transform.transform_LSME.TRANSFORM_LSME('/home/aha/Data/TWFS/rawdata/','/home/aha/Data/TWFS/data/')
	parser.runParse('%d%02d'%(year,month))
	import transform.transform_MD_AUM
	parser = transform.transform_MD_AUM.TRANSFORM_MD_AUM('/home/aha/Data/TWFS/rawdata/','/home/aha/Data/TWFS/data/')
	parser.runParse('%d%02d'%(year,month))
	import transform.transform_MD_Bal
	run("MD_BAL",transform.transform_MD_Bal.parse2,year,month)
	import transform.transform_NC
	parser = transform.transform_NC.TRANSFORM_NC('/home/aha/Data/TWFS/rawdata/','/home/aha/Data/TWFS/data/')
	parser.runParse('%d%02d'%(year,month))
	import transform.transform_PFEI
	run("PFEI",transform.transform_PFEI.parse_2,year,month)


	FOLDERS = ["Y_BAL","DFEI","MD_BAL","MD_AUM","FD_BAL","NC","CD","AREA_DP","CC","ATM","OC","PFEI","LPPE","LSME","LN","LN_AUM","CL","CL_INFO"]
	isResult = True
	for i in range(0,len(FOLDERS)):
		if FOLDERS[i] == "OC" or FOLDERS[i]=="AREA_DP" or FOLDERS[i]=="DFEI":
			continue
		folder = FOLDERS[i]
		isResult = isResult and validation("/home/aha/Data/TWFS/data/%s/%d%02d.csv"%(folder,year,month))
	return isResult








if __name__ == '__main__':
	year = 102
	month = 07
	#print "Extracting Process is success? %s"%(extract(year,month))
	#print "Trasforming Process is success? %s"%(transform(year,month))
	

