#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    Zenzay's Pi Input/Output Library.

    zpiolib.sensor.ultrasonic_sensor module

    Created by Jens Hansen 2019.

"""

import time
import pigpio
from ..gpio.binary_input import Binary_Input
from ..gpio.gpio_output import GPIO_Output
from ..gpio.consts import TICKS_PER_SEC

SPEED_OF_SOUND_MS = 343.26

class UltraSonic_Sensor(Binary_Input):
    def __init__(self, pi, echo_pin, trigger_pin):
        self._echo_speed = SPEED_OF_SOUND_MS / 2.0 / TICKS_PER_SEC
        self._trg_out = GPIO_Output(pi, trigger_pin)
        self._trg_out.write(0)
        super().__init__(pi, echo_pin)

    @property
    def value(self):
        self._trg_out.write(pigpio.ON)
        time.sleep(0.00001)
        self._trg_out.write(pigpio.OFF)
        rc = self.wait_edge(level=0,timeout=0.02)
        if rc:
            rc *= (self._echo_speed)
        return rc
