#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    Zenzay's RPi Input/Output Library.

    zpiolib.gpio.binary_wave module

    Created by Jens Hansen 2019.

"""

import time
import pigpio
from .gpio_output import GPIO_Output
from .consts import TICKS_PER_SEC

class Binary_Wave(GPIO_Output):
    def __init__(self, pi, pin):
        super().__init__(pi, pin)
        self._pulses = []

    def set_pulse(self, timings=None, usec_units=TICKS_PER_SEC):
        self._pulses = []
        if not timings is None:
            self.add_pulse(timings, usec_units)

    def add_pulse(self, timings, usec_units=TICKS_PER_SEC):
        p1 = 1 << self._pin
        p2 = 0
        for item in timings:
            pulse = pigpio.pulse(p1, p2, int(float(item) * usec_units))
            self._pulses.append(pulse)
            #swap p1 and p2
            #p1, p2 = p2, p1
            p1 += p2
            p2 = p1 - p2
            p1 -= p2

    def start_wave(self, repeat=True, wait=False):
        self._pi.wave_clear()
        self._pi.wave_add_generic(self._pulses)
        wave = self._pi.wave_create()
        if repeat:
            self._pi.wave_send_repeat(wave)
        else:
            self._pi.wave_send_once(wave)
        if wait:
            d = 0.1 * len(self._pulses)
            while self._pi.wave_tx_busy():
                time.sleep(d)
        
    def stop_wave(self):
        if self._pi.wave_tx_busy():
            self._pi.wave_tx_stop()
            self._pi.wave_clear()
        self._pi.write(self._pin, pigpio.OFF)

