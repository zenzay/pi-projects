
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    Zenzay's RPi Input/Output Library.

    zpiolib.gpio.gpio_output module

    Created by Jens Hansen 2019.

"""

import pigpio
import logging

class GPIO_Output():
    def __init__(self, pi, pin):
        self._pi = pi
        self._pin = pin
        try:
            self._pi.set_mode(self._pin, pigpio.OUTPUT)
        except Exception:
            logging.exception("Could not set up gpio output")

    def write(self, value):
        self._pi.write(self._pin, int(value))
