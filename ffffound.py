#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Slurps last pictures in ffffound website. Can be NSFW, but must be nice and random.
"""
import feedparser
import urllib2
import shutil
import os.path


class ffffound(object):
    def __init__(self):
        self.d = feedparser.parse('http://feeds.feedburner.com/ffffound/everyone')

    def __iter__(self):
        for entry in self.d.entries:
            yield entry

if __name__ == "__main__":
    for entry in ffffound():
        path = entry.media_content[0]['url']
        d = urllib2.urlopen(path)
        name = path.split('/')[-1]
        if not os.path.exists(name):
            print entry.title
            with open(name, 'w') as l:
                shutil.copyfileobj(d, l)
