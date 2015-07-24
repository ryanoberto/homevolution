#!/usr/bin/python
"""
The MIT License (MIT)

Copyright (c) 2014 Leon Jacobs

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
import RPi.GPIO as GPIO
import time
import logging
import sys, traceback
import socket
import json
from flask import Flask, jsonify, abort, make_response, render_template, request
from flask_cors import CORS
from flask.ext.httpauth import HTTPBasicAuth
#from app import app

#Open Config file
f=open('node-config.yml')
config = yaml.safe_load(f)
#config=yaml.load(f)
f.close()

#set my variables with info from the config file
SECRET = config["SECRET"]
PORT = config["SERVER"]["PORT"]
HOST = config["SERVER"]["HOST"]
BUFFER_SIZE = config["SERVER"]["BUFFER_SIZE"]
APPNAME = config["PROGNAME"]
NODENAME = config["NODENAME"]
NODEIP = config["NODEIP"]
LOGFILE = config["LOGFILE"]
LOGFORMAT = config["LOGFORMAT"]
LOG_LEVEL = config["LOG_LEVEL"]
API_DEBUG = config["DEBUG"]

#Logging
logger = logging.getLogger(APPNAME)
hdlr = logging.FileHandler(LOGFILE)

#formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
formatter = logging.Formatter(LOGFORMAT)
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(LOG_LEVEL)
logging.basicConfig()

#Setup my GPIO Stuff
GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)


# Given a specific channel, we return associated output gpio
# 
def channel2output(channel):
	for d in config['DEVICES']:
		if config['DEVICES'][d]['GPIO_IN'] == channel:
			return config['DEVICES'][d]['GPIO_OUT']

# Given a specific output, check its state and toggle it
def toggleOutput(gpioOut):
	GPIO.setup(gpioOut, GPIO.OUT)
	if (GPIO.input(gpioOut) == 1):
		logger.info("Turning " + str(gpioOut) + " on")
		GPIO.output(gpioOut, GPIO.LOW)
	else:
		logger.info("Turning " + str(gpioOut) + " off")
		GPIO.output(gpioOut, GPIO.HIGH)


# Given a specific channel, do something
def doSomething(channel):
	# Find the output for the input
	output = channel2output(channel)
	logger.info("Button Pressed")
	logger.info("Got output: " + str(output) + " for channel: " + str(channel)) 
	toggleOutput(output)


for d in config["DEVICES"]:
	pin_out = config["DEVICES"][d]["GPIO_OUT"]
	pin_in = config["DEVICES"][d]["GPIO_IN"]
	"""
 	Set outputs to off when we start
	"""
	GPIO.setup(pin_out, GPIO.OUT, initial=GPIO.HIGH)
	logger.info("Setting up " + str(pin_out) + " as output and setting to off...")
	#check if in put is set
	if pin_in > 0:
		# set inputs to in
		GPIO.setup(pin_in, GPIO.IN)
		#pull up or pull down examples
		# GPIO.setup(pin_in, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
		# GPIO.setup(pin_in, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        	logger.info("Setting up " + str(pin_in) + " as input...")
        	#check if input is set
		# add events to inputs was 400
		#GPIO.add_event_detect(pin_in, GPIO.BOTH, callback=doSomething);
		#GPIO.add_event_detect(pin_in, GPIO.FAILING, callback=doSomething, bouncetime=300)
		GPIO.add_event_detect(pin_in, GPIO.RISING, callback=doSomething, bouncetime=300);
		#GPIO.wait_for_edge(pin_in, GPIO.RISING)


app = Flask(__name__, static_url_path='')
cors = CORS(app)

@app.route('/')
@app.route('/index')
def index():
	devices = str(config['DEVICES'].keys())
	
	dev = {}
	for o in config['DEVICES']:
		pin = config["DEVICES"][o]["GPIO_OUT"]
		if(GPIO.input(pin) == 0):
			dev[o] = "On"
		else:   
			dev[o] = "Off"
   # Pass the template data into the template node.html and return it to the user
	templateData = {
      	'devs' : dev,
	'nodename' : NODENAME,
	'nodeip' : NODEIP,
	'port' : PORT
      	}		

	return render_template('node.html', **templateData)

"""
API stuff 
"""

#List available devices
@app.route('/api/list', methods = ['GET'])
#@auth.login_required
def get_list():
    #devices = str(config['DEVICES'].keys())
    devices = config['DEVICES'].keys()
    return jsonify( { 'devices': devices } )

#get status of a device
@app.route('/api/<device>/<action>', methods = ['GET'])
def apiaction(device, action):
	if action == "status":
		devices = config['DEVICES'].keys()
    		if device == "all":
			dev = {NODEIP:{}}
			for o in config['DEVICES']:
				pin = config["DEVICES"][o]["GPIO_OUT"]
				if(GPIO.input(pin) == 0):
					#d = o+ " : On"
					#dev.append(d)
					dev[NODEIP][o] = "On"
				else:   
					#d = o+ " : Off"
   					#dev.append(d)
					dev[NODEIP][o] = "Off"
			
			#return jsonify( { dev } )
			return json.dumps(dev)

    		else:   
			pin = config["DEVICES"][device]["GPIO_OUT"]
			if(GPIO.input(pin) == 0):
				logger.info("device " + device + " status on")
				return jsonify({ 'device' : device, 'status': 'on' })
			else:  
				logger.info("device " + device + " status off") 
				return jsonify({ 'device' : device, 'status': 'off' })
	
	#Get the output pin
	pin = config["DEVICES"][device]["GPIO_OUT"]

#Turn on device
	if action == "on":
		if(GPIO.input(pin) == 0):
			logger.info(device + " is already on")
			return jsonify({ 'device' : device, 'status': 'already on' }) 
		else:
		
			GPIO.output(pin, GPIO.LOW)
			#return 'Turned '+ device +' On \n'
			logger.info("Turned " + device + " on")
			return jsonify({ 'device' : device, 'status': 'on' })

#Turn off device
        if action == "off":
		if(GPIO.input(pin) == 1):
			logger.info(device + " is already off")
			return jsonify({ 'device' : device, 'status': 'already off' })
        	else:          
                	GPIO.output(pin, GPIO.HIGH)
			logger.info("Turned " + device + " off")
			return jsonify({ 'device' : device, 'status': 'off' })

app.run(host=HOST, port=PORT, debug=API_DEBUG)


GPIO.cleanup()
