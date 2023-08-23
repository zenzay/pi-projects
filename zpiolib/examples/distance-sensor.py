#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    Zenzay's RPi Input/Output Library.

    Distance-Sensor Example - Using an HC-SR04 Ultrasonic Sensor Module to measure distances.

    Created by Jens Hansen 2019.

    Note: These sensors rely on the ultrasonic pulse hitting a firm and even surface - resulting in a nice echo - otherwise you'll get rubbish readings.

"""

import sys
import time
import pigpio

sys.path.append("../") # Appending sys-path with parent folder, so we can find the zenpiolib module
from zpiolib.sensor.ultrasonic_sensor import UltraSonic_Sensor

TRIGGER_PIN = 23
ECHO_PIN = 24

if __name__ == '__main__':
    pi = pigpio.pi()
    if not pi.connected:
        print("Unable to connect to pigpio daemon!")
        exit(0)

    ds = UltraSonic_Sensor(pi, ECHO_PIN, TRIGGER_PIN)
    try:
        while True:
            print(f"Distance: {ds.value:.4f} metres")
            time.sleep(1)
    except KeyboardInterrupt:
        print(" - Bye!")
    finally:
        pi.stop()
