#!/usr/bin/env python
# -*- coding: utf-8 -

from __future__ import print_function, unicode_literals
import requests
import argparse
import logging
import sys
from time import sleep

from gps3 import gps3
from .pollution_sensor import PollutionSensor
from .utils import cleanup_gps_dict


logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%m/%d/%y %H:%M:%S',)
logger = logging.getLogger(__name__)


def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--sdevice", help="Sensor device node (e.g. /dev/ttyUSB0)",
        default="/dev/ttyUSB0")
    parser.add_argument("-g", "--gpsd_host", help="GPSd host address", default="127.0.0.1")
    parser.add_argument("-p", "--gpsd_port", help="GPSd host port", default=2947)
    parser.add_argument("-j", "--gpsd_protocol", help="GPSd protocol", default="json")
    parser.add_argument("-t", help="Pause for t seconds before reading the sensors",
        default=5, type=int)
    parser.add_argument("-u", "--url", 
        help="POST to this url. If empty, the script will only print out the values")
    parser.add_argument("-l", "--loglevel", help="Log level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO")
    return parser.parse_args()


def run():
    try:
        args = setup_args()
        logger.setLevel(getattr(logging, args.loglevel.upper()))
        logger.debug("Args: %s", args)

        gpsd_socket = gps3.GPSDSocket()
        logger.info("Connecting to GPSd service")
        gpsd_socket.connect(args.gpsd_host, args.gpsd_port)
        try:
            gpsd_socket.watch(gpsd_protocol=args.gpsd_protocol)
        except (OSError, IOError) as e:
            logger.critical("Can't connect to GPSd service. Is it running and listening on %s:%s",
                args.gpsd_host, args.gpsd_port)
            sys.exit(1)
        else:
            logger.info("Connected to GPSd service")
            data_stream = gps3.DataStream()
            pollution_sensor = PollutionSensor(args.sdevice)
            for new_data in gpsd_socket:
                if new_data:
                    data_stream.unpack(new_data)
                    gps_data = cleanup_gps_dict(data_stream.TPV)
                    logger.debug("GPS reports %s", gps_data)
                    if gps_data.get('lat') or True:
                        ps_data = pollution_sensor.read()
                        if not ps_data:
                            continue
                        gps_data.update(ps_data)
                        logger.debug("Data Ready to be sent: %s", gps_data)
                        if args.url:
                            r = requests.post(args.url, data=gps_data)
                            logger.info("Server responded %s" % r.status_code)
                            if not r.ok:
                                logger.error("Server response:")
                                logger.error(r.content)
                        else:
                            logger.info("Reporting PM10:%(pm10)s PM2.5:%(pm25)s at LAT: %(lat)s LNG: %(lon)s, ALT: %(alt)sm",
                                gps_data)
                    else:
                        logger.info("GPS reports incomplete data %s. Sleeping.",
                            gps_data)
                    sleep(args.t)
    except (KeyboardInterrupt, SystemExit) as err:
        logger.info("Bye!")

