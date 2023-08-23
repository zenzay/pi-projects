#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    Zenzay's RPi Input/Output Library.

    zpiolib.gpio.binary_output module

    Created by Jens Hansen 2019.

"""

from .gpio_output import GPIO_Output

class Binary_Output(GPIO_Output):
    def __init__(self, pi, pin):
        super().__init__(pi, pin)

