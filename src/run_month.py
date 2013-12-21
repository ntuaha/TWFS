# -*- coding: utf-8 -*- 
import os

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
	




if __name__ == '__main__':
	print extract(102,07)
