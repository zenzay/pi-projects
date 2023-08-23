#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    Zenzay's RPi Input/Output Library.

    zpiolib.tools.circular_list module

    Created by Jens Hansen 2019.

"""

class Circular_List():
    def __init__(self, list_size):
        self._size = list_size
        self._index = 0
        self._list = []

    def add_item(self, value):
        if len(self._list) < self._size:
            self._list.append(value)
        else:
            self._list[self._index] = value
            self._index += 1
            if self._index >= self._size:
                self._index = 0

    def get_list(self):
        return self._list
