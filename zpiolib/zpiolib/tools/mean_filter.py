#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    Zenzay's RPi Input/Output Library.

    zpiolib.tools.mean_filter module

    Created by Jens Hansen 2019.

"""

from .circular_list import Circular_List

class Mean_Filter(Circular_List):
    def __init__(self, window_size):
        super().__init__(window_size)

    @property
    def value(self):
        return sum(self._list) / len(self._list)
