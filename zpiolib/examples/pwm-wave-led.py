#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Zenzay's RPi Input/Output Library.

    PWM-Wave-LED Example - Using PWM to get a LED to pulse in waves

    Created by Jens Hansen 2019.

"""

import sys
import signal
import pigpio

sys.path.append("../") # Appending sys-path with parent folder, so we can find the zenpiolib module
from zpiolib.led.pwm_wave_led import PWM_Wave_LED

LED_PIN = 20

if __name__ == '__main__':
    pi = pigpio.pi()
    if not pi.connected:
        print("Unable to connect to pigpio daemon!")
        exit(0)

    led = PWM_Wave_LED(pi, LED_PIN)
    try:
        print ("Blink. Transition=0s. Delay=1s. Enter to start.")
        input()
        led.turn_on(brightness=[1,0], transition=0, delay=1, wait=False)
        print("Enter to stop")
        input()
        led.turn_off()
        print ("Pulse. Transition=1s. Delay=0s. Enter to start.")
        input()
        led.turn_on(brightness=[1,0], transition=1, delay=0, wait=False)
        print("Enter to stop")
        input()
        led.turn_off()

        print ("Growing/fading Pulse. Transition=0.5s. Delay=0s. Enter to start. Ctrl-C to quit")
        input()
        pl = []
        for i in range(10):
            pl.append((i+1)/10)
            pl.append(0)
        for i in range(10):
            pl.append(0)
            pl.append(1- (i+1)/10)

        led.turn_on(brightness=pl, transition=.5, delay=0, wait=False)

        signal.pause()

    except KeyboardInterrupt:
        print(" - Bye!")
    finally:
        led.turn_off()
        pi.stop()
