#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Zenzay's RPi Input/Output Library.

    Binary-Wave-LED Example - Blinking a LED with precise timing

    Created by Jens Hansen 2019.

"""

import sys
import signal
import pigpio

sys.path.append("../") # Appending sys-path with parent folder, so we can find the zpiolib module
from zpiolib.led.binary_wave_led import Binary_Wave_LED

LED_PIN = 20

if __name__ == '__main__':
    pi = pigpio.pi()
    if not pi.connected:
        print("Unable to connect to pigpio daemon!")
        exit(0)

    led = Binary_Wave_LED(pi, LED_PIN)

    try:
        print("Blink LED 5 times. On for 0.5 sec and off for 0.2 sec. Enter to start.")
        input()
        led.turn_on((.5,.2), repeat=5, wait=True)

        print("Next up is a more elaborate blinking session, using a longer wave. Enter to start. Ctrl-C to Quit")
        input()
        #set up pulse-list [on, off, on, off, on, off]
        pl = []
        for i in range(8):
            j = float(i/20) + 0.1
            pl.append(j)
            pl.append(j/2)

        for i in range(8):
            j = (8 - i) / 20 + 0.1
            pl.append(j)
            pl.append(j/2)

        led.turn_on(pl, repeat = -1)   #repeat forever
        signal.pause()

    except KeyboardInterrupt:
        print(" - Bye!")
    finally:
        led.turn_off()
        pi.stop()
