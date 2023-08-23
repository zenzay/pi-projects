#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    Zenzay's Pi Input/Output Library.

    zpiolib.sensor.binary_sensor module

    Created by Jens Hansen 2019.

"""

import time
from ..gpio.binary_trigger import Binary_Trigger

class Binary_Sensor(Binary_Trigger):
    def __init__(self, pi, pin, throttle=0, min_triggers=1, trg_window=1):
        super().__init__(pi, pin, throttle, min_triggers, trg_window)

    def wait_no_trigger(self, cooldown=0):
        c = 0
        t = time.perf_counter()
        while True:
            if self.get_trigger():
                c = 0
            c += 1
            if c > cooldown:
                break
            time.sleep(1)
        return int(time.perf_counter() - t)

