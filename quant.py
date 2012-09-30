#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Use pngquant to extract a weighted palette from a picture.

"""
import os
import colorsys
from cStringIO import StringIO
import Image


class Color(object):
    def __init__(self, rgb, weight):
        self.rgb = rgb
        self.weight = weight
        hsv = colorsys.rgb_to_hsv(rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)
        self.hue = hsv[0]
        self.saturation = hsv[1]

    def __cmp__(self, other):
        return cmp(self.hue, other.hue)

    def __repr__(self):
        return "<Color %s>" % str(self.rgb)

    def hexa(self):
        return "%x%x%x" % self.rgb


def quantize(path, color):
    pipe = os.popen("cat %s | pngquant -nofs %i" % (path, color), "r")
    img = Image.open(StringIO(pipe.read()))
    w, h = img.size
    size = w * h
    colors = [Color(c[1], 1.0 * c[0] / size) for c in img.convert("RGB").getcolors()]
    sorted(colors)
    return colors

if __name__ == "__main__":
    import sys
    print "<html><table><tr>"
    for color in quantize(sys.argv[1], 8):
        print '<td bgcolor="#%s" width="50">&nbsp;</td>' % color.hexa()
    print "</tr></table></html>"
