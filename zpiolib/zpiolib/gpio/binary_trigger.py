
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    Zenzay's RPi Input/Output Library.

    zpiolib.gpio.binary_trigger module

    Created by Jens Hansen 2019.

"""

import threading
import pigpio
from .gpio_input import GPIO_Input
from .consts import TICKS_PER_SEC

class Binary_Trigger(GPIO_Input):
    def __init__(self, pi, pin, throttle=0, min_triggers=1, trg_window=1):
        self._throttle_us = throttle * TICKS_PER_SEC
        self._trg_count = 0
        self._trg_min = min_triggers
        self._trg_window = trg_window
        self._last_tick = 0
        self._event = threading.Event()
        super().__init__(pi, pin, self._cbf, callback_edge=pigpio.RISING_EDGE, pull_up_down=pigpio.PUD_DOWN)
        self._pi.set_glitch_filter(pin, 100)

    def get_trigger(self):
        r = self._event.is_set()
        self._event.clear()
        return r

    def wait_trigger(self, timeout=None):
        t = 0
        while True:
            self._trg_count = 0
            self._event.clear()
            if self._event.wait(self._trg_window):
                return True
            if timeout:
                t += self._trg_window
                if t >= timeout:
                    return False

    def _cbf(self, gpio, level, tick):
        if pigpio.tickDiff(self._last_tick, tick) <= self._throttle_us:
            return

        self._last_tick = tick
        self._trg_count += 1
        if self._trg_count >= self._trg_min:
            self._event.set()
