#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Mathieu Lecarme <mathieu@garambrogne.net>"

import colorsys
import Image


def rgb2hsv(rgb):
    "rgb to hsv conversion with value between 0 and 255"
    tmp = colorsys.rgb_to_hsv(rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)
    return (int(tmp[0] * 255), int(tmp[1] * 255), int(tmp[2] * 255))


def hsv2rgb(hsv):
    "hsv to rgb conversion with value between 0 and 255"
    tmp = colorsys.hsv_to_rgb(hsv[0] / 256.0, hsv[1] / 256.0, hsv[2] / 256.0)
    return (int(tmp[0] * 255), int(tmp[1] * 255), int(tmp[2] * 255))


class Color(object):

    def __init__(self, hue, saturation, quantity=0):
        self.hue = hue
        self.saturation = saturation
        self.quantity = quantity

    def __len__(self):
        return self.quantity

    def __add__(self, other):
        h = (self.hue * self.quantity) + (other.hue * other.quantity) / (self.quantity + other.quantity)
        s = (self.saturation * self.quantity) + (other.saturation * other.quantity) / (self.quantity + other.quantity)
        return Color(h, s, self.quantity + other.quantity)

    def __repr__(self):
        return "<Color %i, %i, %i>" % (self.hue, self.saturation, self.quantity)

    def __cmp__(self, other):
        return cmp(self.quantity, other.quantity)

    def distance(self, other):
        """Vectorial distance between two colors."""
        return pow(pow(self.hue - other.hue, 2) + pow(self.saturation - other.saturation, 2), 0.5)

    def incr(self):
        self.quantity += 1


class ColorMap(object):
    """a 256 x 256 matrix, hue, saturation, with frequency as value
    name: name of the file
    max: is the max value
    data: is the matrix
    pixels: number of pixels
    """
    def __init__(self, path):
        image = Image.open(path)
        self.name = '.'.join(path.split('/')[-1].split('.')[:-1])
        self.data = {}
        for h in range(256):
            self.data[h] = {}
            for s in range(256):
                self.data[h][s] = 0
        width, height = image.size
        self.pixels = width * height
        self.max = 0
        self.colors = {}
        for x in range(width):
            for y in range(height):
                point = image.getpixel((x, y))
                h, s, v = rgb2hsv(point)
                self.data[h][s] += 1
                self.max = max(self.data[h][s], self.max)
                if v > 5 and v < 250:
                    if (h, s) not in self.colors:
                        self.colors[(h, s)] = Color(h, s)
                    self.colors[(h, s)].incr()

    def __getitem__(self, key):
        return self.data[key]


if __name__ == "__main__":
    import sys
    colormap = ColorMap(sys.argv[1])
    print colormap.name, colormap.max
    c = colormap.colors.values()
    c.sort()
    print c
