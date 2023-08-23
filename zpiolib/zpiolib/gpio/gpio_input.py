
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    Zenzay's RPi Input/Output Library.

    zpiolib.gpio.gpio_input module

    Created by Jens Hansen 2019.

"""

import pigpio
import logging

class GPIO_Input():
    def __init__(self, pi, pin, callback_func, callback_edge=pigpio.EITHER_EDGE, pull_up_down=None ):
        self._pi = pi
        self._pin = pin
        try:
            self._pi.set_mode(self._pin, pigpio.INPUT)
            if not pull_up_down is None:
                self._pi.set_pull_up_down(self._pin, pull_up_down)
            self._pi.callback(self._pin, callback_edge, callback_func)
        except Exception:
            logging.exception("Could not set up gpio input")
