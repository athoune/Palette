#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
from numpy import zeros


def colormap(path, size=8):
    cmd = ['convert', path, '-colorspace', 'sRGB', '-colorspace', 'Lab', '-format', '%c', 'histogram:info:-']
    # convert 51963fc1422ea82f6df3deefcea66b9ee7892630_m.jpg -colorspace LAB -format %c histogram:info:-
    pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    m = zeros([size, size], int)
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
                #print b / d, a / d, b, a
                m[b / d][a / d] += n
    coeff = 256 * 256
    return m * coeff / t, black * coeff / t, white * coeff / t


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        m, b, w = colormap(sys.argv[1])
        print m
        print b, w
    elif len(sys.argv) == 3:
        m1, b1, w1 = colormap(sys.argv[1])
        m2, b2, w2 = colormap(sys.argv[2])
        m = m1 - m2
        print abs(m)
