"""
The MIT License (MIT)

Copyright (c) 2014 Ryan Oberto

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
import yaml
import time
import logging
import json
import re
import urllib2
import urllib
import sys, traceback
import subprocess
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from urllib2 import Request, urlopen, URLError

#Open Config file
f=open('master-config.yml')
config = yaml.safe_load(f)
#config=yaml.load(f)
f.close()


#set my variables with info from the config file
APPNAME = config["PROGNAME"]
LOGFILE = config["LOGFILE"]
LOGFORMAT = config["LOGFORMAT"]
LOG_LEVEL = config["LOG_LEVEL"]
DEBUG = config["DEBUG"]
ZM = config["ZM"]["SUPPORT"]
ZMHOST = config["ZM"]["HOST"]

#Logging
logger = logging.getLogger(APPNAME)
hdlr = logging.FileHandler(LOGFILE)
#formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
formatter = logging.Formatter(LOGFORMAT)
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(LOG_LEVEL)
logging.basicConfig()


def list():
        cur = g.db.execute('select name, url from zoneminder')
	zoneminder = [dict(name=row[0], url=row[1] ) for row in cur.fetchall()]
	#zoneminder = [dict(name=row[0], url=row[1]) for row in cur.fetchall()]
        #nodes = [r[0] for r in cur.fetchall()]
        
	return zoneminder
	

def get_cameras():

        ret_data = { 'Name': None, 'Id': None}
        if ZM == True:
		try:
			cur = g.db.execute('select * from zoneminder')
			zhost = [r[0] for r in cur.fetchall()]
			cur = g.db.execute('select * from zoneminder')
			zm = cur.fetchall()
			for row in zm:
   				zhost = row[1]
   				zurl = row[2]
			#zhost = config["ZM"]["HOST"]
                	zport = config["ZM"]["PORT"]
                	#zurl = config["ZM"]["URL"]
			print "Getting cameras from " + zhost
			url = "http://"+ zhost +"/"+ zurl +"monitors.json"
                	data = json.load(urllib2.urlopen(url))

                	# prints the full request output
                	#print json.dumps(data , sort_keys=True,indent=4, separators=(',', ': '))
                	if 'error' in data:
                        	logger.info('Error ')
				ret_data = "error"
                	else:
				ret_data = {}
				int=0
				for i in data['monitors']:
					ID = data['monitors'][int]['Monitor']['Id']
					NAME = data['monitors'][int]['Monitor']['Name']
					ret_data[NAME] = ID
					int += 1
			#print ret_data
        		return ret_data
		except URLError, e:
			e = re.sub('[(){}<>]', '', str(e))
			print e
                        #logger.error('Problem with Zoneminder module or connecting to zoneminder server, Module will be ignored')
			ret_data = e
			return ret_data
	else:
			return False
		
