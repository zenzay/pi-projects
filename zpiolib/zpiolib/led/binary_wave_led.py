#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    Zenzay's Pi Input/Output Library.

    zpiolib.led.binary_wave_led module

    Created by Jens Hansen 2019.

"""

from ..gpio.binary_wave import Binary_Wave

class Binary_Wave_LED(Binary_Wave):
    def __init__(self, pi, pin):
        super().__init__(pi, pin)

    def turn_on(self, timings=None, repeat=0, wait=False):
        if not timings is None:
            self.set_pulse(timings)
            for i in range(repeat-1):
                self.add_pulse(timings)

            self.start_wave(repeat=(repeat == -1), wait=wait)
        else:
            self.write(1)

    def turn_off(self):
        self.stop_wave()
