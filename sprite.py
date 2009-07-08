#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Mathieu Lecarme <mathieu@garambrogne.net>"

#import rabbyt
import math
from colors import ColorMap, hsv2rgb

class Circle(object):
	def __init__(self, x, y, r, color):
		self.x = x *1.0
		self.y = y *1.0
		self.bounding_radius = r
		self.bounding_radius_squared = r*r
		self.color = color

class Packet(object):
	def __init__(self, h, s, size):
		self.h = h
		self.s = s
		self.size = size
	def __repr__(self):
		return "<Packet h:%i s:%i #%i>" % (self.h, self.s, self.size)
	def __cmp__(self, other):
		return self.size.__cmp__(other.size)
	def squared_distance(self,other):
		deltah = abs(self.h - other.h) % 128
		deltas = self.s - other.s
		return deltas*deltas + deltah*deltah

def palette(colormap, size = 256, huescale = 16, saturationscale =16):
	data = {}
	maxi = 0
	for h in range(huescale):
		data[h] = {}
		for s in range(saturationscale):
			data[h][s] = 0
			for hh in range(256 / huescale):
				for ss in range(256 / saturationscale):
					data[h][s] += colormap[h*huescale + hh][s*saturationscale + ss]
			maxi = max(maxi, data[h][s])
	print maxi, data
	packet = colormap.pixels / size
	print packet
	done = []
	todo = []
	for h in range(huescale):
		for s in range(saturationscale):
			n = data[h][s]
			while n > packet:
				done.append(Packet(h*huescale, s*saturationscale, packet))
				n -= packet
			if n > 0:
				todo.append(Packet(h*huescale, s*saturationscale, n))
	todo.sort()
	todo.reverse()
	print "todo", todo
	print
	print "done", done
	#while, todo.pop, pas de revers, todo[-1]
	prems = todo[0]
	shorter = todo[1]
	shorter_dist = prems.squared_distance(shorter)
	for other in todo[2:]:
		distance = prems.squared_distance(other)
		if distance < shorter_dist:
			shorter_dist = distance
			shorter = other
	print prems, shorter, math.sqrt(shorter_dist)
	

if __name__ == "__main__":
	import sys
	colormap = ColorMap(sys.argv[1])
	palette(colormap)
