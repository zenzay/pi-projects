#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Zenzay's RPi Input/Output Library.

    Binary-LED Example - Blinking a Binary LED

    Created by Jens Hansen 2019.

"""

import sys
import time
import pigpio

sys.path.append("../") # Appending sys-path with parent folder, so we can find the zpiolib module
from zpiolib.led.binary_led import Binary_LED

LED_PIN = 20

if __name__ == '__main__':

    pi = pigpio.pi()
    if not pi.connected:
        print("Unable to connect to pigpio daemon!")
        exit(0)
    
    led = Binary_LED(pi, LED_PIN)
    print("Blinking LED. Ctrl-C to stop.")
    try:
        while True:
            led.toggle()
            time.sleep(0.5)
    except KeyboardInterrupt:
        print(" - Bye!")
    finally:
        led.turn_off()
        pi.stop()
