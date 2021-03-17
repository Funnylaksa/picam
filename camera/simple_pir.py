import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor


time.sleep(10)

while True:
    i=GPIO.input(11)
    print(i)
    time.sleep(1)
