#!/usr/bin/env python

import sys
import time
import RPi.GPIO as GPIO

DEVICE_ID='28-03146b771aff'
DEVICE_FILE='/sys/bus/w1/devices/%s/w1_slave' % (DEVICE_ID)

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
        GPIO.output(2,GPIO.HIGH)
        time.sleep(on)
    if off > 0:
        GPIO.output(2,GPIO.LOW)
        time.sleep(off)

def p(temp, target, kp):
    d = target - temp
    if d < 0:
        return 0
    power = d / target * kp
    return power

def i(prev, now, target, ki):
    if prev == 0:
        return 0
    d1 = target - now
    d2 = target - prev
    if d1 < 0:
        return 0
    if d2 < 0:
        d2 = 0
    return (d1 + d2) * 10 / 2 * ki


def main():
    if len(sys.argv) < 2:
        print('usafge: %s TARGET_TEMPERTURE' % (sys.argv[0]))
        sys.exit(0)
    target = float(sys.argv[1])
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(2, GPIO.OUT)
    prev=0
    while True:
        temp = read_temp()
        pg = p(temp, target, 2.7)
        ig = i(prev, temp, target, 0.005)
        power = pg + ig
        if power > 0:
            power += 0.13
        prev = temp
        print t, temp, power
        sys.stdout.flush()
        output(power)
        t += 10

if __name__ == "__main__":
    main()
