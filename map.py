#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import struct
from numpy import zeros


def colormap(path, size=8):
    "Build a matrix of color, black and white colors. Size is the size sampling."
    # imagemagick convert image colorspace from sRGB to CIELab
    # and build an histogram
    cmd = ['convert', path, '-colorspace', 'sRGB', '-colorspace', 'Lab', '-format', '%c', 'histogram:info:-']
    pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    m = zeros([size, size], int)  # empty matrix
    d = 256 / size
    t = 0
    black = 0
    white = 0
    for line in pipe.stdout.readlines():
        ll = line.strip().split(' ')
        if len(ll) > 1:
            n = int(ll[0][:-1])
            t += n
            color = [int(i) for i in ll[-1][4:-1].split(',')]
            l, a, b = color
            if l < 5:
                black += n
            elif l > 250:
                white += n
            else:
                m[b / d][a / d] += n
    coeff = 1000
    # Size doesn't matter, values are comparable
    return m * coeff / t, black * coeff / t, white * coeff / t


def palette(colormap, distance=10):
    # TODO filter with a thresold, group colors with kmeans
    # TODO palette distance, sums of shortest distance between each color from one
    # palette to the other
    pass

if __name__ == "__main__":
    import sys
    import os.path
    if len(sys.argv) == 1:
        import glob
        for img in glob.glob('images/*.jpg'):
            data = 'datas/%s.data' % img.split('/')[-1]
            if os.path.exists(data):
                continue
            m, b, w = colormap(img)
            with open(data, 'w') as d:
                values = list(m.flatten()) + [b, w]
                print img
                print values
                d.write(struct.pack('i' * len(values), *values))
    elif len(sys.argv) == 2:
        m, b, w = colormap(sys.argv[1])
        print m
        print b, w
    elif len(sys.argv) == 3:
        m1, b1, w1 = colormap(sys.argv[1])
        m2, b2, w2 = colormap(sys.argv[2])
        m = m1 - m2
        print abs(m).sum() + abs(b1 - b2) + abs(w1 - w2)
