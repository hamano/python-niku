#!/usr/bin/env python

import sys
import time
import RPi.GPIO as GPIO

DEVICE_ID='28-03146b771aff'
DEVICE_FILE='/sys/bus/w1/devices/%s/w1_slave' % (DEVICE_ID)
GPIO_RELAY=21
DEBUG=False

def read_temp():
    try:
        file = open(DEVICE_FILE)
        lines = file.readlines()
        temp = lines[1].split('t=')[1]
        return float(temp) / 1000
    except Exception as e:
        print e
        return 100

def output(power):
    if power > 1:
        power = 1
    on = power * 10
    off = (1 - power) * 10
    if on > 0:
        GPIO.output(GPIO_RELAY, GPIO.HIGH)
        time.sleep(on)
    if off > 0:
        GPIO.output(GPIO_RELAY, GPIO.LOW)
        time.sleep(off)

def p(temp, target, kp):
    d = target - temp
    if d < 0:
        return 0
    power = d / target * kp
    return power

def i(hist, target, ki):
    s = 0
    for i in range(len(hist)-1):
        d1 = target - hist[i]
        d2 = target - hist[i+1]
        s += (d1 + d2) / 2 * ki
    return s

def main():
    if len(sys.argv) < 2:
        print('usafge: %s TARGET_TEMPERTURE' % (sys.argv[0]))
        sys.exit(0)
    target = float(sys.argv[1])
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_RELAY, GPIO.OUT)
    hist = []
    prev=0
    t=0
    while True:
        temp = read_temp()
        hist.insert(0, temp)
        if len(hist) > 7:
            hist.pop()
        pg = p(temp, target, 3)
        ig = i(hist, target, 0.01)
        if DEBUG:
            print("pg: %f" % (pg))
            print("ig: %f" % (ig))
            print(hist)
        power = pg + ig
        if power > 0:
            power += 0.1
        prev = temp
        print t, temp, power
        sys.stdout.flush()
        output(power)
        t += 10

if __name__ == "__main__":
    main()
