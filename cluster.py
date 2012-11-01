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
    for data in glob.glob('datas/*.data'):
        blob = open(data, 'r').read()
        v = array(struct.unpack('i' * (len(blob) / 4), blob))
        datas.append(([data], 1, v))
    return datas


def reducator(datas, distmax=200):
    while True:
        _, shorter = reduce(datas, distmax)
        if shorter is None:
            return datas
        i, j = shorter
        datas.remove(i)
        datas.remove(j)
        datas.append(fusion(i, j))


if __name__ == "__main__":
    with open('cluster.html', 'w') as f:
        f.write('<html><head><body>')
        for a in reducator(load_data()):
            print a[0]
            if len(a[0]) > 1:
                f.write('<div style="border: thin red dotted; margin: 5px">')
                for aa in a[0]:
                    f.write('<img style="max-height: 128px; margin-right: 5px" src="images/%s"/>' % aa.split('/')[-1][:-5])
                f.write('</div>\n')
        f.write('</body></html>')
