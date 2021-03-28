import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor


time.sleep(10)

triggered = False
while True:
    sensor_val=GPIO.input(11)
    print(sensor_val)
 
    # 4 positive sensor reading in 9 counts -> capture footage 
    if triggered:
        if sensor_val:
            sensor_val_count += 1
            if sensor_val_count % 4==0:
                print('trigger!')
                trigger_count = 1
        elif trigger_count == 9:
            triggered = False
            trigger_count = 0
        else: 
            trigger_count+=1    
        print('trig_count, sensor_val_count:', trigger_count, sensor_val_count)
 
    #init trigger for 1st positive sensor reading 
    if sensor_val and triggered==False:
        trigger_count = 1
        triggered = True
        sensor_val_count = 1
        print('trig_count, sensor_val_count:', trigger_count, sensor_val_count)
    time.sleep(1)
