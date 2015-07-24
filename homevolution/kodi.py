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
#from apscheduler.scheduler import Scheduler
import logging
import json
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
PORT = config["SERVER"]["PORT"]
HOST = config["SERVER"]["HOST"]
APPNAME = config["PROGNAME"]
LOGFILE = config["LOGFILE"]
LOGFORMAT = config["LOGFORMAT"]
LOG_LEVEL = config["LOG_LEVEL"]
DEBUG = config["DEBUG"]
KODI = config["KODI"]["SUPPORT"]
KODI_API_OPT = config["KODI"]["API_OPT"]
ZM = config["ZM"]["SUPPORT"]
NODES = config["NODES"].keys()
VN = config["VN"]
ALARM = config["ALARM"]["SUPPORT"]

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
        cur = g.db.execute('select name, port from kodi')
        kodi = [dict(name=row[0],port=row[1]) for row in cur.fetchall()]
        print kodi
        return kodi

def nowplaying(KODI):

        ret_data = { 'now_playing': None, 'now_playing_image': None}
	print list()
        if list():
		try: 

                	#khost = config["KODI"]["HOST"]
                	#kport = config["KODI"]["PORT"]
			cur = g.db.execute('select * from kodi')
                        zhost = [r[0] for r in cur.fetchall()]
                        cur = g.db.execute('select * from kodi')
                        kodi = cur.fetchall()
			for row in kodi:
                                khost = row[1]
                                kport = row[2]
			#whats playing
			
                	query = """{"jsonrpc": "2.0","method": "Player.GetItem","params": {"properties": ["title","album","artist","season","episode","duration","showtitle","tvshowid","thumbnail","file","fanart","streamdetails"],"playerid": 1},"id": "VideoGetItem"}"""
                	query = urllib.quote_plus(query)
                	url = "http://"+ khost +":"+ kport +"/jsonrpc?request="+query

                	data = json.load(urllib2.urlopen(url))
			print khost
			print kport
                	# prints the full request output
                	#print json.dumps(data , sort_keys=True,indent=4, separators=(',', ': '))

                	#test = data['error']['message']

                	if 'error' in data:
                        	ret_data['now_playing_image'] = " "
                        	ret_data['now_playing'] = "Nothing"
                        	logger.info('Nothing Playing')
                	#if 'error' in data:
                	#       print "poo"
                	#       sys.exit(1)
                	else:
                        	#if 'result' in data:
                        	thumbnail = data['result']['item']['thumbnail']
                        	thumbnail = urllib.unquote(thumbnail).decode('utf8')
                        	ret_data['now_playing_image'] =  thumbnail.replace('image://','')
                        	ret_data['now_playing'] = data['result']['item']['title']
                        	logger.info('Now playing '+ ret_data['now_playing'])

                #print thumbnail
                #print title
		except URLError, e:
			e = re.sub('[(){}<>]', '', str(e))
			#print "Problem with kodi module"
			logger.error(e)

        return ret_data
