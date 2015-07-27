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

"""
Voice Notification Module
"""



import logging
import urllib2
import urllib
import sys, traceback
import subprocess

#Create a funtion to speak notifications
#need to fix this so you can pass any argumnet and it will be spoken
def speak(action):
        text = action
	#print text
        """
	If we can get to the internet we use google translate else espeak
        """
	try :
                stri = "http://translate.google.com"
                data = urllib.urlopen(stri)
                #print "Connected"
                subprocess.call('wget -q -U Mozilla "http://translate.google.com/translate_tts?tl=en&q='+text+'" -O /tmp/action.mp3' ,shell=True)
                subprocess.call ('mpg123 -h 10 -d 11 /tmp/action.mp3', shell=True)
                #subprocess.call ('rm /tmp/*.mp3', shell=True)
        except:
                #logger.info("Cant connect to google translate" ,er)
                subprocess.call('espeak '+text, shell=True)
		
#        logger.info("Turning " +device+" "+action)

#def action(device,action):
#	text="Turning "+device+" "+action
#	print text
#	speak(text)
	
#action("pool","on with you")
