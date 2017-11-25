#!/usr/bin/env python
# -*- coding: utf-8 -

from __future__ import print_function, unicode_literals
import requests
import argparse
import logging
from .pollution_sensor import PollutionSensor

logging.basicConfig(format='[%(asctime)s] %(levelname)-8s: %(message)s', datefmt='%m/%d/%y %H:%M:%S',)
logger = logging.getLogger(__name__)


def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--sdevice", help="Sensor device node (e.g. /dev/ttyUSB0)",
        default="/dev/ttyUSB0")
    parser.add_argument("-u", "--url", 
        help="POST to this url. If empty, the script will only print out the values")
    parser.add_argument("-l", "--loglevel", help="Log level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO")
    parser.add_argument("-p", "--powersaving", help="Powersaving",
        action="store_true")
    parser.add_argument("-s", "--sysnode", help="System node for the usb - for powersaving (e.g. /sys/bus/usb/devices/usb1)",
        default="/sys/bus/usb/devices/usb1")
    return parser.parse_args()


def run():
    args = setup_args()
    logger.setLevel(getattr(logging, args.loglevel.upper()))
    logger.debug("Args: %s", args)

    pollution_sensor = PollutionSensor(args.sdevice,
        powersaving=args.powersaving, sysnode=args.sysnode)
    sensor_read = pollution_sensor.read()
    logger.debug("Pollution sensor said %s", sensor_read)
