#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    Zenzay's RPi Input/Output Library.

    zpiolib.gpio.spi_channel module

    Created by Jens Hansen 2019. Updated 2023.

"""

import logging
from .consts import SPI_BAUD_DEF

class SPI_Channel():
    def __init__(self, pi, channel=0, baud=SPI_BAUD_DEF, flags=0):
        self._pi = pi
        try:
            self.hchannel = self._pi.spi_open(channel, baud, flags)
        except Exception:
            logging.exception("Could not open SPI channel")

    def write_registers(self, data):
        try:
            for i in range(0, len(data), 2):
                data[i] &= 0x7F
            self._pi.spi_xfer(self.hchannel, data)
        except Exception as _:
            self.close()
            logging.exception("Could not write to SPI registers")

    def read_registers(self, reg, count):
        try:
            c, d = self._pi.spi_xfer(self.hchannel, [reg|0x80] + [0]*count)
            if c > 0:
                return c-1, d[1:]
            else:
                return c, d
        except Exception as e:
            logging.exception(e)
            return None

    def close(self):
        self._pi.spi_close(self.hchannel)
