#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import colorsys
import math

import Image
import ImageDraw

class zimage:
	"manipulation d'image"

	def __init__(self, image):
		self.name = '.'.join(image.split('.')[:-1])
		self.mode = "RGB"
		self.values = []
		self.debug = 0
		self.min = [0,0,0]
		self.amplitude = [1,1,1]
		self.image = Image.open(image)
		(self.l,self.h) = self.image.size

	def toHSV(self):
		self.mode = "HSV"
		for x in range(self.l):
			if self.debug:
				print "#", 
			self.values.append([])
			for y in range(self.h):
				point = self.image.getpixel((x,y))
				self.values[x].append(colorsys.rgb_to_hsv(point[0]/255.0,point[1]/255.0,point[2]/255.0))
	def saveCouches(self):
		for a in range(3):
			self.saveCouche(a)
	def saveCouche(self,couche):
		im = Image.new("L",(self.l,self.h))
		for x in range(self.l):
			if self.debug:
				print "@", 
			for y in range(self.h):
				im.putpixel((x,y),int(self.values[x][y][couche]*256))
		im.save("couche__%s.png" % couche)
	def bands(self):
		band = {}
		maxi = 0
		for h in range(256):
			band[h] = {}
			for s in range(256):
				band[h][s] = 0
		for x in range(self.l):
			for y in range(self.h):
					h = int(self.values[x][y][0]*255)
					s = int(self.values[x][y][1]*255)
					band[h][s] +=1
					maxi = max(maxi, band[h][s])
		return maxi, band
	def bandmap(self):
		maxi, bands = self.bands()
		maxi = math.log(maxi)
		print maxi
		im = Image.new('RGBA', (512,512))
		draw = ImageDraw.Draw(im)
		draw.ellipse((0,0,512,512),(0,0,0,255))
		for h in range(256):
			angle = h * math.pi / 128
			for s in range(256):
				if bands[h][s] != 0:
					v = math.log(bands[h][s])/maxi
					r,g,b = colorsys.hsv_to_rgb(h/256.0, s/256.0, v *0.5 + 0.5)
					#im.putpixel((h,s),(int(r*256), int(g*256), int(b*256)))
					draw.point((
						math.sin(angle) * v *256 + 256,
						math.cos(angle) * v *256 + 256
					), (int(r*256), int(g*256), int(b*256)))
		im = im.resize((256,256), Image.ANTIALIAS)
		im.save('%s__map.png' % self.name)

		im = Image.new('RGBA', (512,512))
		draw = ImageDraw.Draw(im)
		draw.ellipse((0,0,512,512),(0,0,0,255))
		m = 0
		hues = {}
		for h in range(256):
			hues[h] = 0
			for s in range(256):
				hues[h] += bands[h][s] * math.log(s+1)
			m = max(m, hues[h])
		m = math.log(m)
		avant = None
		for h in range(256):
			angle = h * math.pi / 128
			if hues[h] != 0:
				r,g,b = colorsys.hsv_to_rgb(h/256.0, 0.75, 0.75)
				pos = (math.sin(angle) * math.log(hues[h]) / m *256 + 256, math.cos(angle) * math.log(hues[h]) / m *256 + 256 )
				if avant != None:
					draw.line([avant, pos], "white")
				avant = pos
				draw.line([(256,256), pos], (int(r*256), int(g*256), int(b*256)))
		im = im.resize((256,256), Image.ANTIALIAS)
		im.save('%s__star.png' % self.name)
	def reference(self):
		im = Image.new('RGB', (256,256))
		for h in range(256):
			for s in range(256):
				r,g,b = colorsys.hsv_to_rgb(h/256.0, s/256.0, 0.5)
				im.putpixel((h,s),(int(r*256), int(g*256), int(b*256)))
		im.save('palette.png')

for a in sys.argv[1:]:
	print a
	img = zimage(a)
	img.toHSV()
	img.bandmap()
#img.reference()
#print img.values