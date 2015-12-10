#!/usr/bin/env python

import sys
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)

DEVICE_ID='28-03146b771aff'
DEVICE_FILE='/sys/bus/w1/devices/%s/w1_slave' % (DEVICE_ID)
TARGET_TEMP = 60

def read_temp():
    try:
        file = open(DEVICE_FILE)
        lines = file.readlines()
        temp = lines[1].split('t=')[1]
        return float(temp) / 1000
    except e:
        return -1

t=0
while True:
    temp = read_temp()
    on = temp < TARGET_TEMP
    print t, temp, on
    sys.stdout.flush()
    if on:
        GPIO.output(2,GPIO.HIGH)
    else:
        GPIO.output(2,GPIO.LOW)
    time.sleep(1)
    t+=1
