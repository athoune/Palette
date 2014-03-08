#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from skimage.data import imread
from skimage.color import rgb2hsv, lab2rgb
from skimage.transform import resize
from sklearn.cluster import MeanShift, estimate_bandwidth

from scipy.spatial import distance
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.cluster import AffinityPropagation


def colors(path):
    "yield x, y value from a resized image."
    img = rgb2hsv(resize(imread(path), (256, 256)))
    return img.reshape((256 * 256, 3))

def convert(s, vmin=0.2, vmax=0.8):
    a = s.transpose()
    v = a[2]
    mask = (v >= vmin) & (v <= vmax)
    img2 = s[mask].transpose()
    h = img2[0] * (2 * np.pi)
    s = img2[1]
    x = np.cos(h) * s
    y = np.sin(h) * s
    r = np.empty(img2.shape)
    r[0] = x
    r[1] = y
    return r.transpose()

def unconvert(xy):
    "restore values"
    xy = xy.transpose()
    r = np.empty(xy.shape)
    x, y = xy[0], xy[1]
    r[0] = np.arctan2(y, x) / (2 * np.pi)
    teta = r[0]

    mask = r[0] < 0
    r[0] += np.where(r[0] < 0,
        np.ones(xy.shape[1]),
        np.zeros(xy.shape[1]))
    
    r[1] = (xy[0] ** 2 + xy[1] ** 2) ** 0.5
    r[2] = 0.75
    return r.transpose()

def mean_shift(X):
    bandwidth = estimate_bandwidth(X, quantile=0.15, n_samples=500)
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(X)
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_
    return labels, cluster_centers


def dbscan(X):
    D = distance.squareform(distance.pdist(X))
    S = 1 - (D / np.max(D))

    db = DBSCAN(eps=0.95, min_samples=100).fit(S)
    core_samples = db.core_sample_indices_
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    print n_clusters_
    print core_samples


def affinity(X):
    af = AffinityPropagation(preference=-50).fit(X)
    cluster_centers_indices = af.cluster_centers_indices_
    labels = af.labels_

    n_clusters_ = len(cluster_centers_indices)
    print cluster_centers_indices


def l(abz):
    "restore a L value for a,b values."
    return [[75.0, ab[0], ab[1]] for ab in abz]


if __name__ == "__main__":
    import sys
    X = colors(sys.argv[1])

    labels, cluster_centers = mean_shift(X)
    labs = l(cluster_centers)
    rgbs = lab2rgb([labs])

    with file('toto.html', 'w') as f:
        f.write('<html><body><table><tr>')
        for rgb in rgbs[0]:
            color = [int(c * 256) for c in rgb]
            print color
            f.write('<td style="background:rgb(%i, %i, %i); width:64px; height:64px;">&nbsp;</td>' % tuple(color))
        f.write('</tr></table><img src="%s"/></body></html>' % sys.argv[1])
