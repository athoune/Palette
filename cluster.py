#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import struct
from numpy import array


def distance(a, b):
    return abs(a - b).sum()


def fusion(a, b):
    names = a[0] + b[0]
    weight = a[1] + a[2]
    histo = (a[2] * a[1] + b[2] * b[2]) / weight
    return names, weight, histo


def reduce(datas, distmax=3000):
    distmin = distmax
    shorter = None
    for i in datas:
        for j in datas:
            if i == j:
                continue
            d = distance(i[2], j[2])
            if d < distmin:
                shorter = (i, j)
                distmin = d
    return distmin, shorter


#def cluster(data, distmax=20):

def load_data():
    datas = []
    for data in glob.glob('*.data'):
        blob = open(data, 'r').read()
        v = array(struct.unpack('i' * (len(blob) / 4), blob))
        datas.append(([data], 1, v))
    return datas


if __name__ == "__main__":
        print reduce(load_data())
