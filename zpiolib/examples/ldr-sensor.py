#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    Zenzay's RPi Input/Output Library.

    LDR-Sensor Example - Using an Light Diode Resistor to measure light levels + utilizing a Median Filter to smooth out readings

    Created by Jens Hansen 2019.

"""

import sys
import time
import pigpio

sys.path.append("../") # Appending sys-path with parent folder, so we can find the zenpiolib module
from zpiolib.sensor.ldr_sensor import LDR_Sensor
from zpiolib.tools.median_filter import Median_Filter

LDR_PIN = 5

if __name__ == '__main__':
    pi = pigpio.pi()
    if not pi.connected:
        print("Unable to connect to pigpio daemon!")
        exit(0)

    filter = Median_Filter(window_size=5)
    ldr = LDR_Sensor(pi, LDR_PIN)
    try:
        while True:
            br = ldr.brightness
            print(f"brightness : {br}")
            if br >= 0:
                filter.add_item(br)
            print(f"    median : {filter.value}")
            time.sleep(1)
    except KeyboardInterrupt:
        print(" - Bye!")
    finally:
        pi.stop()
