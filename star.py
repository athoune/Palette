#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Image
import ImageDraw
import math

from colors import ColorMap, hsv2rgb

def blackCircle(size):
	im = Image.new('RGBA', (size*2,size*2))
	draw = ImageDraw.Draw(im)
	draw.ellipse((0,0,size*2,size*2),(0,0,0,255))
	return im, draw

def hue_map(colormap, size=256):
	im, draw = blackCircle(size)
	maxi = math.log(colormap.max)
	for h in range(256):
		angle = h * math.pi / 128
		for s in range(256):
			if colormap[h][s] != 0:
				v = math.log(colormap[h][s])/maxi
				rgb = hsv2rgb((h, s, 128))
				#im.putpixel((h,s),(int(r*256), int(g*256), int(b*256)))
				draw.point((
					math.sin(angle) * v * size + size,
					math.cos(angle) * v * size + size
				), rgb)
	im = im.resize((size,size), Image.ANTIALIAS)
	im.save('%s__map.png' % colormap.name)

def star(colormap, size=256, white=True):
	im, draw = blackCircle(size)
	m = 0
	hues = {}
	for h in range(256):
		hues[h] = 0
		for s in range(256):
			hues[h] += colormap[h][s] * math.log(s+1)
		m = max(m, hues[h])
	m = math.log(m)
	avant = None
	for h in range(256):
		angle = h * math.pi / 128
		if hues[h] != 0:
			rgb = hsv2rgb((h, 192, 192))
			pos = (math.sin(angle) * math.log(hues[h]) / m *size + size, math.cos(angle) * math.log(hues[h]) / m *size + size )
			if avant != None and white:
				draw.line([avant, pos], "white")
			avant = pos
			draw.line([(size,size), pos], rgb)
	im = im.resize((size,size), Image.ANTIALIAS)
	im.save('%s__star.png' % colormap.name)

if __name__ == "__main__":
	import sys
	colormap = ColorMap(sys.argv[1])
	hue_map(colormap)
	star(colormap)