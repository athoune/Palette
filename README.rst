Palette
=======

Palette is tool for showing color usages on a picture.

Map
---
horizontaly, the hue, verticaly, the saturation. It's experimental.

Star
----
A color wheel, the length of the ray is proportional to the hue.

Install
=======

PIL_ , the Python Imaging Library is used.

Usage
=====
Standard image formats are handled::

  ./palette.py toto.png

Will generate toto__star.png and toto__map.png.

You can use more than one picture in the command line::

  ./palette.py a.png b.png c.jpg d.tif

.. _PIL: http://www.pythonware.com/products/pil/