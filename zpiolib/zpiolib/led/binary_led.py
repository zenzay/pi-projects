#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    Zenzay's Pi Input/Output Library.

    zpiolib.led.binary_led module

    Created by Jens Hansen 2019.

"""

from ..gpio.binary_output import Binary_Output

class Binary_LED(Binary_Output):
    def __init__(self, pi, pin):
        super().__init__(pi, pin)
        self._state = 0

    def turn_on(self):
        self._state = 1
        self.write(self._state)

    def turn_off(self):
        self._state = 0
        self.write(self._state)

    def toggle(self):
        self._state = 1 - self._state
        self.write(self._state)
