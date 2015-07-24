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
from time import gmtime, strftime
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import json
import urllib2
import urllib
import sys, traceback
import subprocess
from urllib2 import Request, urlopen, URLError
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

#import homevolution.voice as voice
from homevolution.device import action, get_devices

###

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
KODI_API_OPT = config["KODI"]["API_OPT"]
ZM = config["ZM"]["SUPPORT"]
NODES = config["NODES"].keys()
VN = config["VN"]
ALARM = config["ALARM"]["SUPPORT"]
SCHEDULE = config['SCHEDULES']
SCHEDULE_TIME = config['SCHEDULE']


#Logging
logger = logging.getLogger(APPNAME)
hdlr = logging.FileHandler(LOGFILE)
#formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
formatter = logging.Formatter(LOGFORMAT)
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(LOG_LEVEL)
logging.basicConfig()

sched = BackgroundScheduler()
sched.start()

#This function is used to turn devices on or off for the scheduler
# need to fix this to allow multiple nodes
def wakeup():
	time = strftime("%H:%M")
	date = strftime("%d %B")
	day = strftime("%A")
	text = "Good morning Family"
	voice.speak(text)
	text = "It is "+time+" on "+day+" the "+date
	voice.speak(text)
	text = "Time to get up"
	voice.speak(text)
	#play song on tv,
	# if dark turn on bedroom lights

#Create wakeup Schedule	
#sched.add_cron_job(schedules,args=[name], month=month, day_of_week=dow, hour=hour, minute=minute, name=name)		
	
def schedules(name):
        for s in config["SCHEDULES"][name]:
                #Get GPIO pin
                #If set to turn on
                if config["SCHEDULES"][name][s] == "On":
                        logger.info("Turning " +s+" "+config["SCHEDULES"][name][s]+" its "+name)
                        action('192.168.1.50',s,'on')
                 	#action(node,s,'on')
			# GPIO.output(pin,GPIO.LOW)
                #If set to turn off
                elif config["SCHEDULES"][name][s] == "Off":
                        logger.info("Turning " +s+" "+config["SCHEDULES"][name][s]+" its "+name)
                        action('192.168.1.50',s,'off')
			#action(node,s,'off')
                        # GPIO.output(pin,GPIO.HIGH)
                else:
                        logger.error('Dont understand the status for '+s)

#This will take the list from the config file and auto generate the schedules to cron.
#
for sc in config['SCHEDULE'].keys():
        name = sc
        month = config['SCHEDULE'][sc]['MONTH']
        dow = config['SCHEDULE'][sc]['DAYOFWEEK']
        hour = config['SCHEDULE'][sc]['HOUR']
        minute = config['SCHEDULE'][sc]['MINUTE']
        #print name, month, dow, hour, minute
        logger.info("Creating Schedule for " + name )
	print "Creating Schedule for " + name
	sched.add_job(schedules,trigger="cron",args=[name],month=month, day_of_week=dow, hour=hour, minute=minute, name=name)
	
#Build a dictionary of schedules and the time when they turn on or off
def gettime(sname):
        ret_getschedule={}

        for shed ,v in config['SCHEDULES'].iteritems():
		HRS = config['SCHEDULE'][shed]['HOUR']
		MINS = config['SCHEDULE'][shed]['MINUTE']
		#NAME = shed+' '+HRS+':'+MINS
		NAME = shed
		ret_getschedule[NAME] = {}
		ret_getschedule[NAME]['DEVICES'] = {}
		#print 'time = '+HRS+':'+MINS
		#print 'shed = ' +shed
		#print v
		for nk, nv in v.iteritems():
			#print NAME
			#print nk, nv
                        ret_getschedule[NAME]['DEVICES'][nk] = nv
		
		#print ret_getschedule
        return ret_getschedule

#gettime('sname')

#Turns off output at 6:00
#sched.add_cron_job(schedules,args=['SUNRISE'], day_of_week='*', hour='17', minute='35')
#Turns on output at 17:30
#sched.add_cron_job(lambda: schedules("SUNSET"), day_of_week='*', hour='17', minute='34')

#sched.add_cron_job(lambda: kodi(), day_of_week="*", hour="*", minute="5")
test = sched.get_jobs()
#print sched.print_jobs()

def getrun(sname):
	ret_getrun={}
	for i in sched.get_jobs():
		#print 'schedule' +str(i)
		schd = str(i)
		schdU = schd.upper()
		name = schdU.split(' ')[0]
		atpos = schdU.find('NEXT')
		sppos = schdU.find(')',atpos)
		run = schdU[atpos:sppos]
		#print name, run
		ret_getrun[name] = run
	#print ret_getrun		
	return ret_getrun	
