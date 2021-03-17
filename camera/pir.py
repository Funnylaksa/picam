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
logging.basicConfig(filename="/home/pi/flask/log//app." + date_string + ".log", 
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
        dt = count/60
        logger.info("Not triggered for past {dt} mins".format(dt=dt))
        #count = 0
    
    if sensor_value:
        now = datetime.now()
        dt_string = now.strftime("%Y%m%d_%H%M%S")
        print("date and time =", dt_string)
        logger.info("PIR Sensor triggered. 5 sec video captured --- ")
        logger.info("---")
        
        photo = "/home/pi/flask/video/{datetime}".format(datetime = dt_string)
        os.system("raspistill -awb greyworld  -o {photo}.jpg -rot 180".format(photo=photo))

        vid = "/home/pi/flask/video/{datetime}".format(datetime = dt_string)
        #os.system("raspivid -awb greyworld -o {vid}.h264 -rot 180 -t 3000".format(vid=vid))
        time.sleep(5)
        #os.system("MP4Box -add {vid}.h264 {vid}.mp4".format(vid=vid))  
        #os.system("rm {vid}.h264".format(vid=vid))
        count = 0

    time.sleep(1)
