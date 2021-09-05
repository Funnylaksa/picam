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
logging.basicConfig(filename="/home/pi/picam/log//app." + date_string + ".log", 
                    format='%(asctime)s %(message)s', 
                    filemode='a') 
  
#Creating an object 
logger=logging.getLogger() 
logger.setLevel(logging.DEBUG) 

#Use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)  
time.sleep(10)       

global count
count = 0
triggered = False


def capture():
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d_%H%M%S")
    print("date and time =", dt_string)
    logger.info("PIR Sensor triggered. Capturing! --- ")
    logger.info("---")
    
    photo = "/home/pi/picam/mega_temp/{datetime}".format(datetime = dt_string)
    os.system("raspistill -awb greyworld  -o {photo}.jpg -rot 180".format(photo=photo))
    
    #vid = "/home/pi/picam/mega_temp/{datetime}".format(datetime = dt_string)
    #os.system("raspivid -awb greyworld -o {vid}.h264 -rot 180 -t 8000".format(vid=vid))
    #time.sleep(8)
    #os.system("MP4Box -add {vid}.h264 {vid}.mp4".format(vid=vid))  
    #os.system("rm {vid}.h264".format(vid=vid))
    count = 0
    time.sleep(3)
    logger.info("Capturing Ends")

# Start here
while True:
    count += 1
    sensor_value = GPIO.input(11)
    
    print ("Sensor value:", sensor_value)    
    if count > 600:
        dt = count/60
        logger.info("Not triggered for past {dt} mins".format(dt=dt))
    
    # 4 positive sensor reading in 9 counts -> capture footage 
    if triggered:
        if sensor_value:
            sensor_value_count+=1
            if sensor_value_count % 5 == 0:
                time.sleep(4)
            if sensor_value_count % 3 == 0:
                capture()
                trigger_count = 1
        elif trigger_count == 9:
            triggered = False
            trigger_count = 0
            logger.info("pir sensor not triggered after 10 seconds. Reset counters"))
        else:
            trigger_count += 1
        print('trigger_count, sensor_val_count:', trigger_count, sensor_value_count)    
        logger.info("trigger_count, sensor_val_count: {}, {}".format(trigger_count, sensor_value_count))
    else:
        logger.info("Not activated")
        
    # init trigger for 1st positive sensor reading
    if sensor_value and triggered==False:
        trigger_count = 1
        sensor_value_count=1
        triggered = True
        capture()
        print('trigger_count, sensor_val_count:', trigger_count, sensor_value_count)
        logger.info("trigger_count, sensor_val_count: {}, {}".format(trigger_count, sensor_value_count))
    time.sleep(1)


