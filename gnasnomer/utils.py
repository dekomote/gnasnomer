#!/usr/bin/env python
# -*- coding: utf-8 -

from __future__ import print_function, unicode_literals
import struct


def bytes2int(bytes):
    return struct.unpack("B", bytes)[0]

def cleanup_gps_dict(d):
    for key, value in d.items():
        if value in [None, "n/a", ""]:
            d[key] = None
    return d
