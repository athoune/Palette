#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from skimage.data import imread
from skimage.color import rgb2lab, lab2rgb
from skimage.transform import resize
from sklearn.cluster import MeanShift, estimate_bandwidth

from scipy.spatial import distance
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.cluster import AffinityPropagation


def colors(path):
    "yield a,b value from a resized image."
    img = rgb2lab(resize(imread(path), (256, 256)))
    for line in img:
        for color in line:
            l = color[0]
            if l < 20 or l > 80:
                continue
            yield color[1:3]


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
    X = np.array(list(colors(sys.argv[1])))

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
