#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    Zenzay's RPi Input/Output Library.

    BH1750-Sensor Example - Using a bh1750 module to measure lux

    Created by Jens Hansen 2019.

"""

import sys
import time
import pigpio

sys.path.append("../") # Appending sys-path with parent folder, so we can find the zenpiolib module
from zpiolib.sensor.bh1750_sensor import BH1750_Sensor

if __name__ == '__main__':
    pi = pigpio.pi()
    if not pi.connected:
        print("Unable to connect to pigpio daemon!")
        exit(0)

    bh1750 = BH1750_Sensor(pi)
    try:
        while True:
            print(f"Lux: {bh1750.value}")
            time.sleep(1)
    except KeyboardInterrupt:
        print(" - Bye!")
    finally:
        pi.stop()
