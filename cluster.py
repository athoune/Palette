#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import struct
from numpy import array

if __name__ == "__main__":
    for data in glob.glob('*.data'):
        blob = open(data, 'r').read()
        v = array(struct.unpack('i' * (len(blob) / 4), blob))
        print v
