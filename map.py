#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
from numpy import array


def colormap(path, size=8):
    cmd = ['convert', path, '-colorspace', 'Lab', '-format', '%c', 'histogram:info:-']
    # convert 51963fc1422ea82f6df3deefcea66b9ee7892630_m.jpg -colorspace LAB -format %c histogram:info:-
    pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    m = array(size * [size * [0]])
    d = 256 / size
    t = 0.0
    for line in pipe.stdout.readlines():
        ll = line.strip().split(' ')
        if len(ll) > 1:
            n = int(ll[0][:-1])
            t += n
            color = [int(i) for i in ll[-1][4:-1].split(',')]
            l, a, b = color
            m[b / d][a / d] += n
    print m * (256 / t)


if __name__ == "__main__":
    import sys
    colormap(sys.argv[1])
