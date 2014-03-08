import unittest

import numpy as np
from skimage.color import rgb2hsv

import colors


def from_hex(h):
    rgb = h[:2], h[2:4], h[4:6]
    return [int(c, 16) for c in rgb]


class TestConvert(unittest.TestCase):
    def setUp(self):
        violet = "5C4EC5"
        pink = "C2377D"
        yellow = "C0D580"
        green = "2A7D48"
        self.sample = np.array([[
            from_hex(violet),
            from_hex(pink),
            from_hex(yellow),
            from_hex(green)]])

    def testPipo(self):
        hsv = rgb2hsv(self.sample / 256.0).reshape((4, 3))
        print hsv
        polar = colors.convert(hsv, 0.0, 1.0)
        print polar
        xy = colors.unconvert(polar)
        print xy


if __name__ == '__main__':
    unittest.main()

