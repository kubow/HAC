#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import subprocess

GPIO.setmode(GPIO.BOARD)
GPIO.setup(13,GPIO.IN,pull_up_down=GPIO.PUD_UP)

btn_down = 0

while True:
    if GPIO.input(13) == True:
        btn_down += 1
        print "Button down for ", 5-btn_down
    else:
        btn_down = 0

    if btn_down > 4:
        print "Shuting down, now!"
        subprocess.call("halt")
        GPIO.cleanup()
        break
    time.sleep(1)