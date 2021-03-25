from flask import Flask, redirect
import RPi.GPIO as GPIO
import time
import signal
import sys
import os
import subprocess
from datetime import datetime
import logging

'''
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
@app.route("/distance")
def distance():
    log = logging.getLogger("/home/pi/picam/app.log")
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
        print ("Distance: %.1f cm" % distance)
        log.info('Hello from distance')
        if distance < 68:
            now = datetime.now()
            dt_string = now.strftime("%d%m%Y%H%M%S")
            os.system("raspivid  -o /home/pi/picam/mega_temp/" + dt_string + ".h264 -rot 180 -t 10000")
            datetime = ("date and time =", dt_string)
            print(datetime)
            log.info(datetime)
        time.sleep(100)
'''


app = Flask(__name__)

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/")
def stream():
    #now = datetime.now()
    #dt_string = now.strftime("%Y%m%d_%H%M%S")
    #photo = "/home/pi/picam/photo/{datetime}".format(datetime = dt_string)
    #os.system("raspistill -awb greyworld  -o {photo}.jpg -rot 180".format(photo=photo))

    subprocess.Popen(["/usr/bin/python3", "/home/pi/picam/camera/streaming.py"], stdout=subprocess.PIPE)
    subprocess.Popen(["/home/pi/picam/camera/killstream.sh"], stdout=subprocess.PIPE)
    time.sleep(3)
    return redirect("http://leetv.ddns.net:8000")

if (__name__ == "__main__"):
    subprocess.Popen(["/usr/bin/python", "/home/pi/picam/camera/pir.py"], stdout=subprocess.PIPE)
    app.run(host='0.0.0.0', port = 5000)
