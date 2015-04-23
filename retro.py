#!/usr/bin/env python
 
# Libraries
import time
import wiringpi2 as wiringpi
import psutil
import atexit

# WiringPi setup
wiringpi.wiringPiSetup()
 
# Setup the LedBorg GPIO pins
PIN_RED = 0
PIN_GREEN = 2
PIN_BLUE = 3
LED_MAX = 100
 
wiringpi.softPwmCreate(PIN_RED,   0, LED_MAX)
wiringpi.softPwmCreate(PIN_GREEN, 0, LED_MAX)
wiringpi.softPwmCreate(PIN_BLUE,  0, LED_MAX)
wiringpi.softPwmWrite(PIN_RED,   0)
wiringpi.softPwmWrite(PIN_GREEN, 0)
wiringpi.softPwmWrite(PIN_BLUE,  0)
 
# A function to set the LedBorg colours
def SetLedBorg(red, green, blue):
    wiringpi.softPwmWrite(PIN_RED,   int(red   * LED_MAX))
    wiringpi.softPwmWrite(PIN_GREEN, int(green * LED_MAX))
    wiringpi.softPwmWrite(PIN_BLUE,  int(blue  * LED_MAX))
 
# A function to turn the LedBorg off
def LedBorgOff():
    SetLedBorg(0, 0, 0)

# Function to handle exit    
def ExitHandler():
    LedBorgOff();

#Turn off leds if script is closed
atexit.register(ExitHandler)

###########
# Globals #
###########
 
# Global var for Index control for the current list
index_co = 0
# Global var for systems list
list = [0]
# Current
current = [0]
 
###########
# Systems #
###########
 
nintendo=['100','200','222']
megadrive=['010','020','121']
gameboyadvance=['202','102','222']
retropie=['010','020', '121']
 
#########
# Funcs #
#########
 
def Check_Processes():
   for proc in psutil.process_iter():
       try:
	   global list
 	   global nintendo
           pinfo = proc.as_dict(attrs=['name'])
           if pinfo.get('name') == 'bash':
               list = gameboyadvance 
       except psutil.NoSuchProcess:
           pass
       else:
           pass

def Next():
   global index_co
   if (index_co < len(list)-1 ):
       index_co = index_co + 1
   else:
       index_co = 0
   return index_co

Check_Processes();

current=list[0]
print current
while True:
	# Check which process is running
	Check_Processes();
	# Sets Current Color
	red=int(current[0])
	green=int(current[1])
	blue=int(current[2])
	#Pulse levels
	levels = range(1, 101)
	levels2 = range(100)
	levels2.reverse()
	levels.extend(levels2)
	# Loop over the levels
	for level in levels:
	   # Get level into the 0 to 1 range
	   level /= 100.0
	   # Set the chosen colour and level
	   SetLedBorg(red * level, green * level, blue * level)
	   # Wait a short while
	   time.sleep(0.01)
	# Next Color on Current System
	current=list[Next()]
	print ('red: ' + str(red) + 'green: ' + str(green) + 'blue: ' + str(blue))
