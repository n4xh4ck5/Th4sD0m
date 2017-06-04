import requests
from urlparse import urlparse
from bs4 import BeautifulSoup
import argparse
from argparse import RawTextHelpFormatter
from urllib2 import urlopen
from contextlib import closing
import json
#define vars
bing_dork=["site:","-site:","language:","domain:","ip:"]
urls = []
urls_clean = []
urls_final =[]
delete_bing=["microsoft","msn","bing"]
#********************************************************#
def banner():
	print "  _____ _   _ _     ___   __   "   
	print " |_   _| |_| | | __|   \ /  \ _ __  " 
	print "   | | | ' \_  _(_-< |) | () | '  \ " 
	print "   |_| |_||_||_|/__/___/ \__/|_|_|_| "
	print "\n"
	print """
	    ** Author: Ignacio Brihuega Rodriguez a.k.a N4xh4ck5
	    ** DISCLAMER This tool was developed for educational goals. 
	    ** The author is not responsible for using to others goals.
	    ** A high power, carries a high responsibility!
	    ** Version 1.0"""

def help():
	print  """ \nTool to identify all domains contained in an IP anonymously

	 			Example of usage: python th4sd0m.py -i DIRECTION_IP -n 4 -e Y """
""" FUNCTION SENDEQUEST """
#Use Bing to obtain all domains contained in an IP
def SendRequest(ip,num,initial):
	iteration = 0
	count_bing=9
	try:
		while (iteration < num):
			iteration = iteration +1
			if initial==True:
				print "\nSearching domains...\n"
				initial = False
				#First search in Bing
				SearchBing = "https://www.bing.com/search?q="+bing_dork[4]+ip
			else:
				#Bring the next Bing results - 50 in each page
				SearchBing = "https://www.bing.com/search?q="+bing_dork[4]+ip+"&first="+str(count_bing)+"&FORM=PORE"
				count_bing=count_bing+50
			try:
				#Use requests to do the search
				response=requests.get(SearchBing,allow_redirects=True)
				parser_html(response.text)	
			except Exception as e:
				print e
				pass
	except Exception as e:
		print e
		pass
#********************************************************#
""" FUNCTION PARSER_HTML"""
def parser_html(content):
	i = 0;
	soup = BeautifulSoup(content, 'html.parser')
	for link in soup.find_all('a'):
		try:
			if (urlparse(link.get('href'))!='' and urlparse(link.get('href'))[1].strip()!=''):
				urls.append(urlparse(link.get('href'))[1])
		except Exception as e:
			#print(e)
			pass	
	try:
		#Delete duplicates
		[urls_clean.append(i) for i in urls if not i in urls_clean] 
	except:
		pass
	try:
		#Delete not domains belongs to target
		for value in urls_clean:
			if (value.find(delete_bing[0])  == -1):
				#Delete Bing's domains
				if (value.find(delete_bing[1])  == -1):
					if (value.find(delete_bing[2])  == -1):
						urls_final.append(value)
	except:
		pass
######FUNCTION EXPORT RESULTS #######
""" FUNCTION EXPORT RESULTS"""
def ExportResults(data):
	#Export the results in json format
	with open ('output.json','w') as f:
		json.dump(data,f)

""" FUNCTION VISU RESULTS """
def VisuResults(ip):
	print "Information about the IP",ip+"\n"
	WhoismyIP(ip)
	print "\nDomains contained in the IP "+ip+" are:"
	#Read the list to print the value in a line
	for i in urls_final:
		if i not in newlist:
			newlist.append(i)
			print "\n"
			print "\t- " + i

"""FUNCTION WhoISMYIP"""
def WhoismyIP(ip):
	url =""
	url = 'http://freegeoip.net/json/'+ip
	try:
	    with closing(urlopen(url)) as response:
	        location = json.loads(response.read())
	        print location
	        location_city = location['city']
	        location_state = location['region_name']
	        location_country = location['country_name']
	        location_zip = location['zipcode']
	except:
		pass
#MAIN
parser = argparse.ArgumentParser(description='This script identifies all domains contained in an IP', formatter_class=RawTextHelpFormatter)
parser.add_argument('-i','--ip', help="The IP which wants to search",required=True)
parser.add_argument('-n','--num', help="Indicate the number of the search which you want to do",required=True)
parser.add_argument('-e','--export', help='Export the results to a json file (Y/N)\n\n', required=False)
args = parser.parse_args()
banner()
help ()
#Asignation from arguments to variables.
initial = True
N = int (args.num)
ip=args.ip
output=args.export
domains=[]
content = ""
if output is None:
	output = 'N'
if ((output != 'Y') and (output != 'N')):
	print "The output option is not valid"
	exit(1)
try:
	content = SendRequest(ip,N,initial)
except:
	pass
newlist=[]
#Call the function to show results
VisuResults(ip)
#verify if the user wants to export results
if output == 'Y':
		#Only it can enter if -e is put in the execution
	ExportResults(newlist)