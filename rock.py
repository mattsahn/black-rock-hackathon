#Need neopixel
 
import time
import  RPi.GPIO as GPIO 
from subprocess import Popen, PIPE, STDOUT
import json

LED_COUNT       = 8
LED_PIN         = 21
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
 
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
 
if __name__ == '__main__':
        # Create neopixel object
        #stick = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        #stick.begin()
 
        #print 'Press Ctrl-c to quit.'
        #colorWipe (stick, Color(150,100,200))
        #colorWipe (stick, Color(0,0,0))

## main program loop right here
## wait for button press to do something

	#initial light show
	proc_led = Popen(['python','/home/pi/Downloads/rpi_ws281x/python/examples/glow_pulse.py','rainbow'],stdout = PIPE, stderr = STDOUT)

	loop = 0
	pulsing = False
        while True: 

		loop = loop + 1
		## check the blog JSON file every 1000000th loop
		if(loop%1000000 == 0):
			loop = 0
			print("check json")
			with open('/home/pi/Downloads/polly_poc/newClips.json') as json_data:
    				d = json.load(json_data)
    				if(d):
					print("json not empty")
					color = d[0]['color']
					print("Color: " + str(color))
					if(pulsing == False):
						print("starting pulse")
						proc_led.terminate()
						if(color==2):
							proc_led = Popen(['python','/home/pi/Downloads/rpi_ws281x/python/examples/glow_pulse.py','holiday'],stdout = PIPE, stderr = STDOUT)
						else:
							proc_led = Popen(['python','/home/pi/Downloads/rpi_ws281x/python/examples/glow_pulse.py','pulse'],stdout = PIPE, stderr = STDOUT)
						pulsing = True
				else:
					print("JSON empty")
					if(pulsing == True):
						print("Back to rainbow")
						proc_led.terminate()
						pulsing = False
						proc_led = Popen(['python','/home/pi/Downloads/rpi_ws281x/python/examples/glow_pulse.py','rainbow'],stdout = PIPE, stderr = STDOUT)

                inputValue = GPIO.input(18)
                if (inputValue == False):
                        print("Button press ")
			proc_led.terminate()

			## play node script depending on pulsing or not
			if(pulsing):
                        	p = Popen(['/home/pi/.nvm/versions/node/v6.10.0/bin/node','/home/pi/Downloads/polly_poc/playClipFromWeb.js']) # play audio
				pulsing = False
			else:
                        	p = Popen(['/home/pi/.nvm/versions/node/v6.10.0/bin/node','/home/pi/Downloads/polly_poc/getBlogPosts.js']) # read blog
				
			proc_led = Popen(['python','/home/pi/Downloads/rpi_ws281x/python/examples/glow_pulse.py','nightrider'],stdout = PIPE, stderr = STDOUT)
			p.wait()
			
                        proc_led.terminate()
			proc_led_off = Popen(['python','/home/pi/Downloads/rpi_ws281x/python/examples/turnoff.py','pulse'],stdout = PIPE, stderr = STDOUT)
			proc_led_off.wait()
			time.sleep(1)
			proc_led = Popen(['python','/home/pi/Downloads/rpi_ws281x/python/examples/glow_pulse.py','rainbow'],stdout = PIPE, stderr = STDOUT)
                        
			print("done with button press section. back to waiting")
