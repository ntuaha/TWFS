# -*- coding: utf-8 -*- 
import os
import sys
import psycopg2
from types import *
reload(sys) 
sys.setdefaultencoding('utf8')


class TWFS_ETL:
	FOLDERS = ["Y_BAL","DFEI","MD_BAL","MD_AUM","FD_BAL","NC","CD","AREA_DP","CC","ATM","OC","PFEI","LPPE","LSME","LN","LN_AUM","CL","CL_INFO"]
	#FOLDERS = ["Y_BAL","MD_BAL","MD_AUM","FD_BAL","NC","CD","AREA_DP","CC","ATM","OC","PFEI","LPPE","LSME","LN","LN_AUM","CL","CL_INFO"]

	def extract(self,year,month):
		from extract.download import Download
		base_path = "/home/aha/Data/TWFS/" 
		#設定其它參數
		CIS = ["4_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1"]
		#CIS = ["2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1","2_1"]
		FOLDERS = ["DFEI","MD_BAL","MD_AUM","FD_BAL","NC","Y_BAL","CD","AREA_DP","CC","ATM","OC","PFEI","LPPE","LSME","LN","LN_AUM","CL","CL_INFO"]
		#FOLDERS = ["MD_BAL","MD_AUM","FD_BAL","NC","Y_BAL","CD","AREA_DP","CC","ATM","OC","PFEI","LPPE","LSME","LN","LN_AUM","CL","CL_INFO"]
		FILES = ["4140","22010","22020","22030","22040","22050","22060","213010","29010","28010","21020","21010","24030","24040","24010","24020","25010","25020"]	
		#FILES = ["22010","22020","22030","22040","22050","22060","213010","29010","28010","21020","21010","24030","24040","24010","24020","25010","25020"]	
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

	def checkFolder(self,folder):
		if os.path.exists(folder) == False:
			os.makedirs(folder)

	def validate_transfromation(self,path):
		if os.path.isfile(path) and os.stat(path).st_size>500:
			print "%s Done!"%(path)
			return True
		else:
			print "%s ERROR!!!!!!!!"%(path)
			return False

	def transform(self,year,month):
		def run(folder,transformFunction,year,month):
			from_path= '/home/aha/Data/TWFS/rawdata/%s/' % (folder)
			to_path = '/home/aha/Data/TWFS/data/%s/' % (folder)
			self.checkFolder(to_path)
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


		
		isResult = True
		for i in range(0,len(self.FOLDERS)):
			if self.FOLDERS[i] == "OC" or self.FOLDERS[i]=="AREA_DP" or self.FOLDERS[i]=="DFEI":
				continue
			folder = self.FOLDERS[i]
			isResult = isResult and self.validate_transfromation("/home/aha/Data/TWFS/data/%s/%d%02d.csv"%(folder,year,month))
		return isResult

	#驗證
	def validate_loading(self,table,year,month):
		conn = psycopg2.connect(database="data", user="aha", password="dataaha305", host="127.0.0.1", port="5432")
		cur = conn.cursor()	
		if table != "PFEI":
			sql = "SELECT DISTINCT count(*) FROM %s where data_dt='%04d-%02d-01';"%(table,year+1911,month)
		else:
			sql = "SELECT DISTINCT count(*) FROM %s where data_ym='%04d-%02d-01';"%(table,year+1911,month)
		cur.execute(sql)
		num = None
		for result in cur.fetchall():
			num = result[0]
		conn.close()
		if num is not NoneType and num>0 :
			print "%s : %d"%(table,num)
			return True
		else:
			print "%s : ERROR"%(table)
			return False


	def load(self,year,month):
		import loading.PFEI
		loading.PFEI.read('/home/aha/Data/TWFS/data/PFEI/%d%02d.csv'%(year,month))
		import loading.md_bal
		loading.md_bal.read('/home/aha/Data/TWFS/data/MD_BAL/%d%02d.csv'%(year,month),"MD_BAL")
		loading.md_bal.read('/home/aha/Data/TWFS/data/MD_AUM/%d%02d.csv'%(year,month),"MD_AUM")
		loading.md_bal.read('/home/aha/Data/TWFS/data/FD_BAL/%d%02d.csv'%(year,month),"FD_BAL")
		loading.md_bal.read('/home/aha/Data/TWFS/data/CD/%d%02d.csv'%(year,month),"CD")
		loading.md_bal.read('/home/aha/Data/TWFS/data/ATM/%d%02d.csv'%(year,month),"ATM")
		import loading.CC
		loading.CC.read('/home/aha/Data/TWFS/data/Y_BAL/%d%02d.csv'%(year,month),"Y_BAL")
		loading.CC.read('/home/aha/Data/TWFS/data/CC/%d%02d.csv'%(year,month),"CC")
		import loading.Cl_Info
		loading.Cl_Info.read('/home/aha/Data/TWFS/data/CL_INFO/%d%02d.csv'%(year,month),"CL_INFO")
		import loading.LSME
		loading.LSME.read('/home/aha/Data/TWFS/data/LSME/%d%02d.csv'%(year,month))
		import loading.Ln_Aum
		loading.Ln_Aum.read('/home/aha/Data/TWFS/data/LN_AUM/%d%02d.csv'%(year,month),"LN_AUM")
		import loading.LN
		loading.LN.read('/home/aha/Data/TWFS/data/LN/%d%02d.csv'%(year,month),"LN")
		import loading.CL
		loading.CL.read('/home/aha/Data/TWFS/data/CL/%d%02d.csv'%(year,month),"CL")

		#FOLDERS = ["Y_BAL","DFEI","MD_BAL","MD_AUM","FD_BAL","NC","CD","AREA_DP","CC","ATM","OC","PFEI","LPPE","LSME","LN","LN_AUM","CL","CL_INFO"]
		isResult = True
		for i in range(0,len(self.FOLDERS)):
			if self.FOLDERS[i] == "OC" or self.FOLDERS[i]=="LPPE"or self.FOLDERS[i]=="AREA_DP" or self.FOLDERS[i]=="DFEI" or self.FOLDERS[i]=="NC":
				continue
			folder = self.FOLDERS[i]
			isResult = isResult and self.validate_loading(folder,year,month)
		return isResult

	def etl(self,year,month):
		isExtract = self.extract(year,month)
		#isExtract = True
		isTransform = self.transform(year,month)
		isLoading = self.load(year,month)
		if isExtract == True and isTransform ==True and isLoading == True:
			Title = "完成"
			Result = "成功"
			Detail = "%4d-%02d Taiwan Finacial Statistics 資料獲得"%(year,month)
			api = '688430041191592'; 
			api_secret = '6bb097ca9fe10f1bca0c1c320232eba2';
			callback_website = 'https://github.com/ntuaha/TWFS/';
			picture_url_tick = 'http://www.iconarchive.com/icons/pixelmixer/basic/64/tick-icon.png';
			facebook_id = '100000185149998';
			cmd = os.popen("/usr/bin/curl -F grant_type=client_credentials -F client_id=%s -F client_secret=%s -k https://graph.facebook.com/oauth/access_token"%(api,api_secret))
			k = cmd.read()
			access_token = k.split("=")[1] 
			work = "/usr/bin/curl -F 'access_token=%s' -F 'message=%s' -F 'name=%s' -F 'picture=%s' -F 'caption=%s' -k https://graph.facebook.com/%s/feed"%(access_token,Detail,Title,picture_url_tick,Result,facebook_id)
			#print work
			cmd = os.popen(work)
		else:
			pass









if __name__ == '__main__':
	#year = 102
	#month = 07
	agent = TWFS_ETL()
	agent.etl(int(sys.argv[1]),int(sys.argv[2]))

	

