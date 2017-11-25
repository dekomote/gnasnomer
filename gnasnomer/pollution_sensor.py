#!/usr/bin/env python
# -*- coding: utf-8 -

from __future__ import print_function, unicode_literals
import os
import logging
import struct
import serial
from .utils import bytes2int


logger = logging.getLogger(__name__)


class PollutionSensor(object):

    def __init__(self, device, powersaving=False, sysnode=None, baudrate=9600):
        self.device = device
        self.powersaving = powersaving
        self.sysnode = sysnode
        self.baudrate = baudrate
        self.ready = False
        self.serial = None

    def init_usb(self):
        logger.debug("Initializing USB Powersaving")
        if self.powersaving and self.sysnode:
            return os.system("echo disabled > %s/power/wakeup"%self.sysnode)
        else:
            logger.debug("Failed to initialize USB Powersaving. Missing sysnode?")

    def turn_on_usb(self):
        logger.debug("Turning USB ON")
        if self.sysnode:
            return os.system("echo on > %s/power/level"%self.sysnode)
        else:
            logger.debug("Failed to turn USB ON. Missing sysnode or USB already ON.")

    def turn_off_usb(self):
        logger.debug("Turning USB OFF")
        if self.sysnode:
            return os.system("echo off > %s/power/level"%self.sysnode)
        else:
            logger.debug("Failed to turn USB OFF. Missing sysnode or USB already OFF.")

    def init_device(self):
        if self.powersaving and self.sysnode:
            self.init_usb()
            self.turn_on_usb()
        if not self.serial:
            logger.info("Initializing pollution sensor device")
            try:
                self.serial = serial.Serial(self.device, baudrate=self.baudrate)
                return self.serial
            except serial.SerialException as e:
                logger.critical(e)
                return False
        else:
            return self.serial

    def read(self):
        if self.init_device():
            read_full = False
            pm25 = 0
            pm10 = 0
            data = []
            try:
                while not read_full:
                    if self.serial.read() == b'\xaa':
                        # FIRST HEADER IS GOOD
                        if self.serial.read() == b'\xc0':
                            # SECOND HEADER IS GOOD
                            for i in range(8):
                                byte = self.serial.read()
                                data.append(bytes2int(byte))

                            if data[-1] == 171:
                                # END BYTE IS GOOD. DO CRC AND CALCULATE
                                if data[6] == sum(data[0:6])%256:
                                    logger.debug("CRC good")
                                pm25 = (data[0]+data[1]*256)/10
                                pm10 = (data[4]+data[3]*256)/10
                                read_full = True
            except serial.SerialException as e:
                logger.critical(e)
                return None
            logger.info("PM 10: %s" % pm10)
            logger.info("PM 2.5: %s" % pm25)
            return {
                "pm10": pm10,
                "pm25": pm25,
            }

    def __del__(self):
        if self.serial:
            logging.info("Closing pollution sensor device")
            self.serial.close()
        if self.powersaving:
            self.turn_off_usb()
