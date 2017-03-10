import urllib2
from xml.etree import ElementTree as etree
#import feedparser
import re
from bs4 import BeautifulSoup
import time
import  RPi.GPIO as GPIO 
from neopixel import *
from subprocess import Popen
 
LED_COUNT       = 8
LED_PIN         = 21
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN,pull_up_down=GPIO.PUD_UP) 

stick = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
stick.begin()

def colorWipe(stick, color, wait_ms=50):
        """ wipe color across display pixel a time """
        for i in range(stick.numPixels()):
                stick.setPixelColor(i, color)
                stick.show()
                time.sleep(wait_ms/1000.0)
 
 
def nightrider(stick, color, wait_ms=70):
        """ Knight raider kitt scanner """
        for i in range(stick.numPixels()):
                stick.setPixelColor(i,color)
                stick.setPixelColor(i-1,dimColor(color))
                stick.show()
                time.sleep(wait_ms/1000.0)
                stick.setPixelColor(i,0)
                stick.setPixelColor(i-1,0)
        # reverse the direction
        for i in xrange(stick.numPixels()-1,-1,-1):
                stick.setPixelColor(i,color)
                stick.setPixelColor(i+1,dimColor(color))
                stick.show()
                time.sleep(wait_ms/1000.0)
                stick.setPixelColor(i,0)
                stick.setPixelColor(i+1,0)
 
def dimColor (color):
        """ Color is an 32-bit int that merges the values into one """
        return (((color&0xff0000)/3)&0xff0000) + (((color&0x00ff00)/3)&0x00ff00) + (((color&0x0000ff)/3)&0x0000ff)
 

print("executing")

blk_file = urllib2.urlopen('https://www.blackrockblog.com/feed/')
#convert to string:
blk_data = blk_file.read()
#close file because we dont need it anymore:
blk_file.close()

#entire feed
blk_root = etree.fromstring(blk_data)
item = blk_root.findall('channel/item')

stories = "Here are the three latest stories from the Blackrock blog: "
num = 1

for entry in item:
	#get description
        stories += " Number " + str(num) + ". "
        stories += entry.findtext('description')
        if num == 3:
            break
        num += 1

stories += " Go to blackrock blog dot com to read the full stories. Goodbye"
print("sending to IFTTT : " + stories)
p = Popen(['/home/pi/.nvm/versions/node/v6.10.0/bin/node','/home/pi/Downloads/polly_poc/read.js',stories]) # something long running
count = 20
while (count > 0): 
        nightrider (stick,Color(255,255,0),65)
        count = count - 1
        #p.terminate()
                      
colorWipe (stick, Color(0,0,0))

print("Done")

