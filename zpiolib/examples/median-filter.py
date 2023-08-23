#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Zenzay's RPi Input/Output Library.

    Median-Filter Example - Feeds random ints to a circular list and spits out the list and median.

    Created by Jens Hansen 2019.

"""

import sys
import random

sys.path.append("../") # Appending sys-path with parent folder, so we can find the zenpiolib module
from zpiolib.tools.median_filter import Median_Filter

if __name__ == '__main__':
    mf = Median_Filter(window_size=5)
    for i in range(0,15):
        n = random.randint(1, 100)
        print(f"New item: {n}")
        mf.add_item(n)
        print(f"List: {mf.get_list()}")
        print(f"Median: {mf.value}")
