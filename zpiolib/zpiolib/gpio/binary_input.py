#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    Zenzay's RPi Input/Output Library.

    zpiolib.gpio.binary_input module

    Created by Jens Hansen 2019.

"""
import time
import threading
import pigpio
from .gpio_input import GPIO_Input
from .consts import TICKS_PER_NANO

class Binary_Input(GPIO_Input):
    def __init__(self, pi, pin, callback_edge=pigpio.EITHER_EDGE, pull_up_down=None):
        self._events = (threading.Event(),threading.Event())
        self._ticks = [0,0]
        super().__init__(pi, pin, self._cbf, callback_edge=callback_edge, pull_up_down=pull_up_down)

    def wait_edge(self, level, timeout=None):
        if level:
            if self._events[pigpio.ON].wait(timeout):
                return pigpio.tickDiff(self._ticks[pigpio.OFF], self._ticks[pigpio.ON])
        else:
            if self._events[pigpio.OFF].wait(timeout):
                return pigpio.tickDiff(self._ticks[pigpio.ON], self._ticks[pigpio.OFF])
        return 0

    def zero_and_wait_edge(self, pin_settle=0.002, timeout=0):
        self._pi.set_mode(self._pin, pigpio.OUTPUT)
        self._pi.write(self._pin, pigpio.OFF)
        time.sleep(pin_settle)
        self._pi.set_mode(self._pin, pigpio.INPUT)
        t = time.perf_counter_ns()
        if timeout != 0:
            if self._events[pigpio.ON].wait(timeout):
                return (time.perf_counter_ns() - t) / TICKS_PER_NANO
        return -1

    def _cbf(self, gpio, level, tick):
        self._events[level].set()
        self._events[1-level].clear()
        self._ticks[level] = tick
