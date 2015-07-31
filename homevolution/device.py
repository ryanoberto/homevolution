#!/usr/bin/python
"""
The MIT License (MIT)

Copyright (c) 2015 Ryan Oberto

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
import re
import logging
import json
import urllib2
import urllib
#import sys, traceback
#import subprocess
from urllib2 import Request, urlopen, URLError
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_cors import CORS

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

#Logging
logger = logging.getLogger(APPNAME)


#This Function will turn a device on or off
def action(node,device,action):
        request = Request('http://'+node+':5000/api/'+device+'/'+action)

        try:
                response = urlopen(request)
                error = response.read()
                print error[559:1000]
                print "Turning "+ device, action
		#if Voice Notifications is enabled.
                #if voice.VN == True:
                #        text = "Turning " +device+ " " +action
                 #       voice.speak(text)
                #print kittens
		#if KN == True:
		#	print "kittens"
        except URLError, e:
                print 'Got an error code:', e

"""
Get a list of nodes from the database
"""

def list_devices():
	cur = g.db.execute('select node from slaves order by id desc')
        nodes = [dict(name=row[0]) for row in cur.fetchall()]
	#nodes = [r[0] for r in cur.fetchall()]
	print nodes
	return nodes


def get_devices():

	cur = g.db.execute('select node from slaves')
	NODES=[r[0] for r in cur.fetchall()]
	dev = {}
        for node in NODES:
		try:
			print "Getting Device and status from "+ node
			logger.info('Getting Devices and status from ' +node)
                	url = Request("http://"+ node +":5000/api/all/status")
                	data = json.load(urllib2.urlopen(url))	
			dev[node] = data
			print "Success"
		
		except URLError, e:
			logger.error(e)
                	e = re.sub('[(){}<>]', '', str(e))
			#Removes the junk and only shows error, problem is I cant find anything
			#e = e.split("]",2)[1]
			dev[node] = e
			print e
	if not dev:
		dev["error"] = "error No device found please add"
		return dev
	else:
		return dev


def check_devices():
	"""
	This will be used to check the heath of each node, for the dashboard

	"""

        cur = g.db.execute('select node from slaves')
        NODES=[r[0] for r in cur.fetchall()]
        dev = {}
        for node in NODES:
                try:
                        print "Getting Device and status from "+ node
                        logger.info('Getting Devices and status from ' +node)
                        url = Request("http://"+ node +":5000/api/all/status")
                        data = json.load(urllib2.urlopen(url))
                        dev[node] = data
                except URLError, e:
                        print e
                        logger.error(e)
                        dev[node] = e
        if not dev:
                dev["error"] = "error No devices found please add"
                return dev
        else:
                return dev


