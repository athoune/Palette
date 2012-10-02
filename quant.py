#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Use pngquant to extract a weighted palette from a picture.
http://pngquant.org/#algorithm

pngnq :
http://pngnq.sourceforge.net/

colormath :
http://code.google.com/p/python-colormath/wiki/ColorConversions
"""
import os
import colorsys
import math
from cStringIO import StringIO

from colormath.color_objects import RGBColor
import Image
import ImageDraw

from palette import hsv2rgb


class Color(object):
    def __init__(self, rgb, weight):
        self.rgb = rgb
        self.weight = weight
        self.lab = RGBColor(*rgb).convert_to('lab')
        hsv = colorsys.rgb_to_hsv(rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)
        self.hue = hsv[0]
        self.saturation = hsv[1]

    def __cmp__(self, other):
        return cmp(self.hue, other.hue)

    def __repr__(self):
        return "<Color %s>" % str(self.rgb)

    def hexa(self):
        return "%x%x%x" % self.rgb

    def distance(self, other):
        return pow(pow(self.lab.lab_a - other.lab.lab_a, 2) + pow(self.lab.lab_b - other.lab.lab_b, 2), 0.5)
        #return pow(pow(self.saturation - other.saturation, 2) + pow(self.hue - other.hue, 2), 0.5)


def quantize(path, color, thresold=20, quant='pngquant'):
    if quant == 'pngquant':
        cmd = 'pngquant -nofs'
    elif quant == 'pngnq':
        cmd = 'pngnq -n'
    pipe = os.popen("cat %s | %s %i" % (path, cmd, color), "r")
    img = Image.open(StringIO(pipe.read()))
    w, h = img.size
    size = w * h
    colors = [Color(c[1], 1.0 * c[0] / size) for c in img.convert("RGB").getcolors()]
    colors.sort()
    if thresold is None:
        return colors
    last = colors.pop()
    blended = []
    while len(colors):
        ante = colors.pop()
        #print ante.distance(last)
        if ante.distance(last) > thresold:
            blended.append(last)
        last = ante  # blend color
    blended.append(last)
    return blended


def colormap(colors, size=256):
    im = Image.new('RGBA', (size * 2, size * 2))
    draw = ImageDraw.Draw(im)
    #im, draw = wheel.blackCircle(256)

    for h in range(256):
        angle = h * math.pi / 128
        for s in range(256):
            rgb = hsv2rgb((h, s, 255))
            draw.point((
                math.sin(angle) * s / 256 * size + size,
                math.cos(angle) * s / 256 * size + size
            ), rgb)
    im = im.resize((size, size), Image.ANTIALIAS)
    im.save('%s__map.png' % "popo")

if __name__ == "__main__":
    import sys
    colors = quantize(sys.argv[1], 16, 20, 'pngquant')
    print '<html><br><table><tr>'
    for color in colors:
        print '<td bgcolor="#%s" width="50">&nbsp;</td>' % color.hexa()
    print '</tr></table><br><img src="%s"></html>' % sys.argv[1]
    #colormap(colors)
