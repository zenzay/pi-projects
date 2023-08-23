#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    Zenzay's Pi Input/Output Library.

    zpiolib.sensor.bh1750_sensor module

    Created by Jens Hansen 2019.

    Note: Requires the i2c interface to be active. (use raspi-config to enable)
		  also, of course, a bh1750 module hooked up to SDA (gpio2) and SCL (gpio3)

"""
import time
from ..gpio.i2c_bus import I2C_Bus

class BH1750_Sensor(I2C_Bus):
    def __init__(self, pi, bus=1, address=0x23):
        self._filter = filter
        self._LUXDELAY = 0.5
        super().__init__(pi, bus, address)

    @property
    def value(self):
        try:
            self.write_registers([0x10])
            time.sleep(self._LUXDELAY)
            c, d = self.read_registers(0x00, 2)
            v = int.from_bytes(d, byteorder='big', signed=True)
        except Exception:
            v = None

        return v
