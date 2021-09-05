import RPi.GPIO as GPIO
import time
import sys
import os
from datetime import datetime
import logging
  
start = datetime.now()
dt_start_string = start.strftime("%Y%m%d_%H%M%S")  
date_string = start.strftime("%Y%m%d")

#Create and configure logger 
logging.basicConfig(filename="/home/pi/picam/log/app." + date_string + ".log", 
                    format='%(asctime)s %(message)s', 
                    filemode='a') 
  
#Creating an object 
logger=logging.getLogger() 
logger.setLevel(logging.DEBUG) 

#Use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)  
time.sleep(10)       

count = 0
while True:
    count += 1
    sensor_value = GPIO.input(11)
    logger.info("Not activated")
    print ("Sensor value:'", sensor_value)    
    if count > 600:
        logger.info("Not triggered for past 10 mins")
    
    if count == 10:
        now = datetime.now()
        dt_string = now.strftime("%Y%m%d_%H%M%S")
        print("date and time =", dt_string)
        logger.info("PIR Sensor triggered. 5 sec video captured --- ")
        logger.info("---")
        #os.system("raspistill  -o /home/pi/flask/photo/" + dt_string + ".jpg -rot 180")
        #os.system("raspivid -awb greyworld -o /home/pi/flask/video/" + dt_string + ".h264 -rot 180 -t 5000")
        vid = "/home/pi/flask/video/{datetime}".format(datetime = dt_string)
        print(vid) 
        os.system("raspivid -awb greyworld -o {vid}.h264 -rot 180 -t 5000".format(vid=vid))
        os.system("MP4Box -add {vid}.h264 {vid}.mp4".format(vid=vid))  
        os.system("rm {vid}.h264".format(vid=vid))
        count = 0

    time.sleep(1)
