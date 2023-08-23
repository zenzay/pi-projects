#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    Zenzay's Pi Input/Output Library.

    zpiolib.sensor.ldr_sensor module

    Created by Jens Hansen 2019.

    Note: Light Diode Resistors are analogue things and thus we're having to jump through hoops to try and get sensible readings out of it on a Pi.
          This also means that it's pretty inaccurate and can mostly only be utilized in an ON/OFF setting.

    Values:
       -1 -> Timeout reading sensor. It took too long trying to read the sensor - which means that not enough photons hit the sensor within the time-window requested.
       >0 -> The time it took for the sensor to 'fill up' with photons - the lower the value, the brighter it is.

"""

from ..gpio.binary_input import Binary_Input
from ..gpio.consts import TICKS_PER_SEC

class LDR_Sensor(Binary_Input):
    def __init__(self, pi, pin, timeout=1.0):
        self._timeout = timeout
        self._max_read = timeout * TICKS_PER_SEC
        
        super().__init__(pi, pin)

    @property
    def value(self):
        return self.zero_and_wait_edge(timeout=self._timeout)

    @property
    def brightness(self):
        v = self.value
        if v < 0:
            p = 0
        else:
            p = 100 - int(v * 100 / self._max_read)

        return p
