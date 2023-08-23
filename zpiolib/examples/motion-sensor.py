#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Zenzay's RPi Input/Output Library.

    Motion-Sensor (Binary_Sensor) Example - Using a PIR-sensor to detect motion and subsequently waiting for no motion.

    Created by Jens Hansen 2019.

"""

import sys
import pigpio

sys.path.append("../") # Appending sys-path with parent folder, so we can find the zenpiolib module
from zpiolib.sensor.binary_sensor import Binary_Sensor

PIR_PIN = 17

if __name__ == '__main__':
    pi = pigpio.pi()
    if not pi.connected:
        print("Unable to connect to pigpio daemon!")
        exit(0)

    """
    Example 1:
    Setting up a motion sensor using a HC-SR501 PIR module. This module is prone to EMI, so I'm settting a requirement of minimum 2 triggers within a 2 second time window. No throttle as that would delay trigger counting.
    Note1: You can hack the HC-SR501 to trigger faster: https://www.youtube.com/watch?v=juOtoUabyH8
    Note2: You can also feed it 3.3v on one of the trigger jumper-pins instead of 5v on Vin, to make it more resistant to false positives (it seems to work).
    """
    # motion = Binary_Sensor(pi, PIR_PIN, throttle=0, min_triggers=2, trg_window=2)

    """
    Example 2:
    Setting up a motion sensor using a Panasonic PIR Module.
    These guys are very resistent to EMI, but triggers really often, so setting a throttle of 1 second
    """
    motion = Binary_Sensor(pi, PIR_PIN, throttle=1)
    try:
        while True:
            print("Waiting for motion.")
            motion.wait_trigger()
            print("Motion detected!")
            t = motion.wait_no_trigger(cooldown=5)
            print(f"Motion stopped. Duration: {t}s")
    except KeyboardInterrupt:
        print(" - Bye!")
    finally:
        pi.stop()
