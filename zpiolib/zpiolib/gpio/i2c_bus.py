#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    Zenzay's RPi Input/Output Library.

    zpiolib.gpio.i2c_bus module

    Created by Jens Hansen 2019.

"""

import logging

class I2C_Bus():
    def __init__(self, pi, bus, address):
        self._pi = pi
        try:
            self._hbus = self._pi.i2c_open(bus, address)
        except Exception:
            logging.exception("Could not open i2c bus")

    def close(self):
        if self._hbus is not None:
            self._pi.i2c_close(self._hbus)
            self._hbus = None

    def write_registers(self, data):
        try:
            self._pi.i2c_write_device(self._hbus, data)
        except Exception as _:
            self.close()
            logging.exception("Could not write to i2c registers")

    def read_registers(self, reg, count):
        try:
            return self._pi.i2c_read_i2c_block_data(self._hbus, reg, count)
        except Exception as e:
            self.close()
            logging.exception(e)
            return None
