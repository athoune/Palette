#!/usr/bin/env python
# -*- coding: utf-8 -*-

import colorsys

def rgb2hsv(rgb):
	"rgb to hsv conversion with value between 0 and 255"
	tmp = colorsys.rgb_to_hsv(rgb[0]/256.0,rgb[1]/256.0,rgb[2]/256.0)
	return (int(tmp[0]*255),int(tmp[1]*255),int(tmp[2]*255))

class Matrix:
	"a 256 x 256 matrix, hue, saturation, with frequency as value"
	def __init__(self, image):
		self.data = {}
		for h in range(256):
			self.data[h] = {}
			for s in range(256):
				self.data[h][s] = 0
		width, height = image.size
		self.max = 0
		for x in range(width):
			for y in range(height):
				point = image.getpixel((x,y))
				h,s,v = rgb2hsv(point)
				self.data[h][s] += 1
				self.max = max(self.data[h][s], self.max)

if __name__ == "__main__":
	import Image
	import sys
	image = Image.open(sys.argv[1])
	matrix = Matrix(image)
	print matrix.max
	#print matrix.data