#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    Zenzay's RPi Input/Output Library.

    zpiolib.gpio.pwm_output module

    Created by Jens Hansen 2019.

"""

import time
import threading
from .gpio_output import GPIO_Output
from .consts import PWM_RANGE_DEF, PWM_STEP_DEF

class PWM_Output(GPIO_Output):
    def __init__(self, pi, pin, pwm_range=None):
        super().__init__(pi, pin)
        self._pwm_duty = 0
        self._trans_event = threading.Event()
        self._trans_thread = None
        if pwm_range is None:
            self._pwm_range = PWM_RANGE_DEF
        else:
            self._pwm_range = pwm_range
        if self._pwm_range != PWM_RANGE_DEF:
            self._pi.set_PWM_range(self._pin, self._pwm_range)

    def set_value(self, value, transition=None, wait=False):
        self.set_duty(int(float(value) * self._pwm_range), transition, wait)

    def set_duty(self, duty, transition=None, wait=False):
        if duty < 0:
            duty = 0
        if duty > self._pwm_range:
            duty = self._pwm_range

        self._stop_trans()
        if not transition:
            self._pwm_duty = duty
            self._pi.set_PWM_dutycycle(self._pin, self._pwm_duty)
            return
        if wait:
            self._start_trans(duty, transition)
        else:
            self._trans_thread = threading.Thread(target = self._start_trans, args=(duty, transition,))
            self._trans_thread.daemon = True
            self._trans_thread.start()

    def _stop_trans(self):
        if self._trans_event.is_set():
            self._trans_event.clear()
            if not self._trans_thread is None:
                self._trans_thread.join()

    def _start_trans(self, new_duty, transition):
        self._trans_event.set()
        step = PWM_STEP_DEF // transition
        if step < 1:
            step = 1
        delay = float(transition) / float(self._pwm_range + 1) * step
        duty = self._pwm_duty
        if new_duty > duty:
            while self._trans_event.is_set():
                duty += step
                if duty >= new_duty:
                    break
                self._pwm_duty = duty
                self._pi.set_PWM_dutycycle(self._pin, self._pwm_duty)
                time.sleep(delay)
        elif new_duty < duty:
            while self._trans_event.is_set():
                duty -= step
                if duty <= new_duty:
                    break
                self._pwm_duty = duty
                self._pi.set_PWM_dutycycle(self._pin, self._pwm_duty)
                time.sleep(delay)

        self._pwm_duty = new_duty
        self._pi.set_PWM_dutycycle(self._pin, self._pwm_duty)
        self._trans_event.clear()
        self._trans_thread = None
