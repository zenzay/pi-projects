#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    Zenzay's RPi Input/Output Library.

    zenpiolib.gpio.pwm_wave module

    Created by Jens Hansen 2019.

"""

import time
import threading
from .pwm_output import PWM_Output

class PWM_Wave(PWM_Output):
    def __init__(self, pi, pin, pwm_range=None):
        super().__init__(pi, pin, pwm_range)
        self._wave_event = threading.Event()
        self._wave_thread = None
        self._pulses = []

    def set_pulse(self, values, transition=0, delay=0):
        self._pulses = []
        for v in values:
            self.add_pulse(v, transition, delay)

    def add_pulse(self, value, transition=0, delay=0):
        p = { 'v': value, 't': transition, 'd': delay }
        self._pulses.append(p)

    def start_wave(self, wait=False, repeat=True):
        self.stop_wave()
        if wait:
            self._play_wave(repeat)
        else:
            self._wave_thread = threading.Thread(target = self._play_wave, args=(repeat,))
            self._wave_thread.daemon = True
            self._wave_thread.start()

    def stop_wave(self):
        self._stop_trans()
        if self._wave_event.is_set():
            self._wave_event.clear()
            if not self._wave_thread is None:
                self._wave_thread.join()

    def _play_wave(self, repeat):
        d = 0
        t = 0
        self._wave_event.set()
        while self._wave_event.is_set():
            for p in self._pulses:
                t = p['t']
                d = p['d']
                v = p['v']
                self.set_duty(int(float(v) * self._pwm_range), transition=t, wait=True)
                if not self._wave_event.is_set():
                    break
                time.sleep(d)
            if not repeat:
                break
        self._wave_event.clear()
        self._wave_thread = None
