#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    Zenzay's RPi Input/Output Library.

    zpiolib.tools.median_filter module

    Created by Jens Hansen 2019.

"""

from .circular_list import Circular_List

class Median_Filter(Circular_List):
    def __init__(self, window_size):
        super().__init__(window_size)

    @property
    def value(self):
        size = len(self._list)
        index = size // 2
        if size % 2:
            return sorted(self._list)[index]
        return sum(sorted(self._list)[index - 1:index + 1]) / 2
