#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    Zenzay's Pi Input/Output Library.

    zpiolib.led.pwm_led module

    Created by Jens Hansen 2019.

"""

from ..gpio.pwm_output import PWM_Output

class PWM_LED(PWM_Output):
    def __init__(self, pi, pin):
        super().__init__(pi, pin)

    def turn_on(self, brightness=1, transition=1, wait=True):
        self.set_value(value=brightness, transition=transition, wait=wait)

    def turn_off(self, transition=1, wait=True):
        self.set_value(value=0, transition=transition, wait=wait)
