#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    Zenzay's Pi Input/Output Library.

    zpiolib.sensor.dallas_sensor module

    Created by Jens Hansen 2019.

    Note: Requires 1-wire interface to be active. (use raspi-config to enable).

"""

import glob
import time

class Dallas_Sensor():
    def __init__(self):
        self._db_addr = glob.glob('/sys/bus/w1/devices/28*')[0] + '/w1_slave'

    def _read_lines(self):
        f = open(self._db_addr, 'r')
        lines = f.readlines()
        f.close()
        return lines

    @property
    def value(self):
        try:
            lines = self._read_lines()
            while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                lines = self._read_lines()
            e_pos = lines[1].find('t=')
            if e_pos != -1:
                str = lines[1][e_pos+2:]
                r = (float(str) / 1000.0)
        except:
            r = 0
        return round(r,2)
