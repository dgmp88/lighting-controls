#!/usr/bin/env python2.7
# script by Alex Eames http://RasPi.tv
#http://RasPi.tv/2013/how-to-use-soft-pwm-in-rpi-gpio-pt-2-led-dimming-and-motor-speed-control
# Using PWM with RPi.GPIO pt 2 - requires RPi.GPIO 0.5.2a or higher

import RPi.GPIO as GPIO # always needed with RPi.GPIO
from time import sleep  # pull in the sleep function from time module

GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD numbering schemes. I use BCM

red_id = 2
green_id = 24
blue_id = 3


GPIO.setup(red_id, GPIO.OUT)# set GPIO 25 as output for white led
GPIO.setup(green_id, GPIO.OUT)# set GPIO 24 as output for red led
GPIO.setup(blue_id, GPIO.OUT)# set GPIO 24 as output for red led

red = GPIO.PWM(red_id, 100)      # create object red for PWM on port 24 at 100 Hertz
green = GPIO.PWM(green_id, 100)      # create object red for PWM on port 24 at 100 Hertz
blue = GPIO.PWM(blue_id, 100)    # create object white for PWM on port 25 at 100 Hertz


blue.start(0)             
red.start(0)              
green.start(0)

pause_time = 1.0

try:
    while True:
        blue.ChangeDutyCycle(0)
        red.ChangeDutyCycle(100)
        #green.ChangeDutyCycle(100)

        sleep(pause_time)
        red.ChangeDutyCycle(0)
        blue.ChangeDutyCycle(100)
        green.ChangeDutyCycle(0)

        sleep(pause_time)

except KeyboardInterrupt:
    blue.stop()            # stop the white PWM output
    red.stop()              # stop the red PWM output
    green.stop()
    GPIO.cleanup()          # clean up GPIO on CTRL+C exit

