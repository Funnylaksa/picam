import RPi.GPIO as GPIO
import time
import signal
import sys
import os
from datetime import datetime
import logging
  
start = datetime.now()
dt_start_string = start.strftime("%Y%m%d_%H%M%S")  
date_string = start.strftime("%Y%m%d")

#Create and configure logger 
logging.basicConfig(filename="/home/pi/flask/log//app." + date_string + ".log", 
                    format='%(asctime)s %(message)s', 
                    filemode='a') 
  
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

count = 0
timed_earlier = False 
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
    if distance < 120: 
        logger.info("Distance Sensor triggered." + "Distance: %.1f cm" % distance)
        logger.info("---")
        print("Distance Sensor triggered.")
      
        # add start time if no time earlier was recorded 
        if not timed_earlier: 
            start_time = time.time()     
            timed_earlier = True 
        # check if sensor consecutively triggered or possibly false alarm 
        else:
            end_time = time.time()
            duration = end_time - start_time
            if duration < 10:  
                now = datetime.now()
                dt_string = now.strftime("%Y%m%d_%H%M%S")
                logger.info("Distance Sensor triggered. 5 sec video captured --- " + "Distance: %.1f cm" % distance)
                #os.system("raspistill  -o /home/pi/flask/photo/" + dt_string + ".jpg -rot 180")
                os.system("raspivid -awb greyworld -o /home/pi/flask/mega_temp/" + dt_string + ".h264 -rot 180 -t 5000 | tee -a /home/pi/flask/log/app." + date_string + ".log")
                #os.system("raspivid -awb greyworld -o /home/pi/flask/mega_temp/test.h264 -rot 180 -t 5000")
                print('5 sec video')
                timed_earlier = False
            else:
                start_time = time.time()                 
        
    time.sleep(3)
