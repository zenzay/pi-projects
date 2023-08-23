#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    Zenzay's RPi Input/Output Library.

    Dallas-Sensor Example - Using a DS18B20 sensor to measure temperature.

    Created by Jens Hansen 2019.

    Note: Requires 1-wire interface to be active. (use raspi-config to enable).

	Put a 4k7 pull-up resistor on data line to 3.3v, and data line to GPIO 4.

"""

import time
import sys
sys.path.append("../") # Appending sys-path with parent folder, so we can find the zenpiolib module
from zpiolib.sensor.dallas_sensor import Dallas_Sensor

if __name__ == '__main__':
    db = Dallas_Sensor()
    try:
        while True:
            print(f"Temperature: {db.value}")
            time.sleep(1)
    except KeyboardInterrupt:
        print(" - Bye!")

