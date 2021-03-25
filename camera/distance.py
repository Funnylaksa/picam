import RPi.GPIO as GPIO
import time
import signal
import sys
import os
from datetime import datetime
import logging
  
start = datetime.now()
dt_start_string = start.strftime("%Y%m%d_%H%M%S")  

#Create and configure logger 
logging.basicConfig(filename="/home/pi/flask/log//app." + dt_start_string + ".log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w') 
  
#Creating an object 
logger=logging.getLogger() 
logger.setLevel(logging.DEBUG) 


# use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
pinTrigger = 18
pinEcho = 24

def close(signal, frame):
    print("\nTurning off ultrasonic distance detection...\n")
    GPIO.cleanup() 
    sys.exit(0)

signal.signal(signal.SIGINT, close)

# set GPIO input and output channels
GPIO.setup(pinTrigger, GPIO.OUT)
GPIO.setup(pinEcho, GPIO.IN)

while True:
    # set Trigger to HIGH
    GPIO.output(pinTrigger, True)
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(pinTrigger, False)

    startTime = time.time()
    stopTime = time.time()

    # save start time
    while 0 == GPIO.input(pinEcho):
        startTime = time.time()

    # save time of arrival
    while 1 == GPIO.input(pinEcho):
        stopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = stopTime - startTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    logger.info("Distance: %.1f cm" % distance)
    print ("Distance: %.1f cm" % distance)
    if distance < 150:
        now = datetime.now()
        dt_string = now.strftime("%Y%m%d_%H%M%S")
        print("date and time =", dt_string)
        logger.info("Distance Sensor triggered. 5 sec video captured --- " + "Distance: %.1f cm" % distance)
        logger.info("---")
        #os.system("raspistill  -o /home/pi/flask/photo/" + dt_string + ".jpg -rot 180")
        os.system("raspivid  -o /home/pi/flask/mega_temp/" + dt_string + ".h264 -rot 180 -t 5000")

        
    time.sleep(2)
