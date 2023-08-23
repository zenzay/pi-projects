#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Zenzay's RPi Input/Output Library.

    PWM-LED Example - Using PWM to control brightness of a LED

    Created by Jens Hansen 2019.

"""

import sys
import pigpio

sys.path.append("../") # Appending sys-path with parent folder, so we can find the zpiolib module
from zpiolib.led.pwm_led import PWM_LED

LED_PIN = 20

if __name__ == '__main__':
    pi = pigpio.pi()
    if not pi.connected:
        print("Unable to connect to pigpio daemon")
        exit(0)

    led = PWM_LED(pi, LED_PIN)
    try:
        print ("Turn on LED. Brightness 25%. Press Enter to start")
        input()
        led.turn_on(0.25)
        print ("Press Enter to continue")
        input()
        led.turn_off()
        print ("LED Brightness 100%. Transition=4s. Press Enter to start")
        input()
        led.turn_on(transition=4)
        print ("Fade LED out. Transition 0.5s. Press Enter to start")
        input()
        led.turn_off(transition=0.5)
        print ("Pulsate. Transition=1s. Enter to start. Ctrl-C to quit")
        input()
        while True:
            led.turn_on()
            led.turn_off()

    except KeyboardInterrupt:
        print(" - Bye!")
    finally:
        led.turn_off()
        pi.stop()
