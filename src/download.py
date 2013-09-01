import urllib2
import urllib
import time
from datetime import date
import numpy as np
import webbrowser
import os

def download(year,month):
	password = "aruxopq0rliabmUVxillmnWcop79abcdLXpemqeZijklqefgelfqeiIJKprlineYdeaBNyneytthjjlobc93A456hijki"
	random_number = np.random.random_integers(0,len(password)-1,8)
	pwd  = "".join([ password[i] for i in random_number])
	#server_path = "https://survey.banking.gov.tw/statis/stmain.jsp?sys=120&ym=%d%02d&ymt=%d%02d&kind=0&type=2&funid=2050&cycle=0&outmode=3&rdm=%8s" %(year,month,year,month,pwd)
	server_path = "https://survey.banking.gov.tw/statis/2_1_%d%02d%d%02d/22050.xls" % (year,month,year,month)
	client_path = "/Users/aha/Dropbox/Project/Financial/Data/%d%02d.xls" % (year,month)
	cookie_path = '/Users/aha/Dropbox/Project/Financial/Data/cookie0001.txt'
	agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31'
	print server_path
	print client_path
	cmd = 'curl -A "%s" -o %s -D %s %s'% (agent,client_path,cookie_path,server_path)
	os.system(cmd)



if __name__ == '__main__':
	start_year = 80	
	end_year = 102
	for year in range(start_year,end_year+1):
		for month in range(1,13):
			download(year,month)

