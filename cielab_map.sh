#!/bin/sh

convert -size 8x8 -resize 256x256 -filter Point gradient:black-white gradient_a.gif
convert -rotate -90 gradient_a.gif gradient_b.gif
convert  gray.gif gradient_a.gif gradient_b.gif\
           -set colorspace Lab -combine -set colorspace sRGB -rotate 90 palette.png
