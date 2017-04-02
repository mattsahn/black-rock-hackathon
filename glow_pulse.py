# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
from neopixel import *
import sys

# example command line:
# sudo python rock_led.py rainbow 60

# LED strip configuration:
LED_COUNT      = 8      # Number of LED pixels.
LED_PIN        = 21      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
	"""Movie theater light style chaser animation."""
	for j in range(iterations):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, color)
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=75, iterations=1):
	"""Draw rainbow that fades across all pixels at once."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((i+j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def pulse(strip, wait_ms=6, iterations=1):
	"""Draw rainbow that fades across all pixels at once."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, 255)
	strip.show()
	for j in range(256):
		strip.setBrightness(j)
		strip.show()
		time.sleep(wait_ms/1000.0)
	for j in reversed(range(256)):
		strip.setBrightness(j)
		strip.show()
		time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
	"""Draw rainbow that uniformly distributes itself across all pixels."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
	"""Rainbow movie theater light style chaser animation."""
	for j in range(256):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, wheel((i+j) % 255))
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def nightrider(stick, color, wait_ms=60):
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



# Main program logic follows:
if __name__ == '__main__':
	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	# Intialize the library (must be called once before other functions).
	strip.begin()

	print ('Press Ctrl-C to quit.')
	while True:
		# Color wipe animations.
		#colorWipe(strip, Color(255, 0, 0))  # Red wipe
		#colorWipe(strip, Color(0, 255, 0))  # Blue wipe
		#colorWipe(strip, Color(0, 0, 255))  # Green wipe
		# Theater chase animations.
		#theaterChase(strip, Color(127, 127, 127))  # White theater chase
		#theaterChase(strip, Color(127,   0,   0))  # Red theater chase
		#theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
		# Rainbow animations.
		if(len(sys.argv)!=2):
			print("Must pass exactly one argument")
			quit()
		if(sys.argv[1] == 'pulse'):
			print("Pulse!")
			pulse(strip)
		elif(sys.argv[1] == 'rainbow'):
			print("Rainbow!")
			rainbow(strip)
		elif(sys.argv[1] == 'nightrider'):
			print("Nightrider!")
			nightrider(strip,Color(255,0,0),65)
		else:
			print("Need to pass argument of 'pulse' or 'rainbow'")
		#rainbowCycle(strip)
		#theaterChaseRainbow(strip)
