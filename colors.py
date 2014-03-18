#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from skimage.data import imread
from skimage.color import rgb2hsv, hsv2rgb, rgb2luv, luv2rgb
from skimage.transform import resize
from skimage.filter import gaussian_filter
from skimage.segmentation import slic
from sklearn.cluster import MeanShift, estimate_bandwidth

from scipy.spatial import distance
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.cluster import AffinityPropagation


def colors(path):
    "yield x, y value from a resized image."
    img = gaussian_filter(rgb2luv(resize(imread(path), (256, 256))), sigma=0.4, multichannel=True)
    return img.reshape((256 * 256, 3))

def convert(s, vmin=20, vmax=90):
    a = s.transpose()
    L = a[0]
    mask = (L >= vmin) & (L <= vmax)
    img2 = s[mask].transpose()
    return img2[:, 1:].transpose()

def unconvert(xy):
    "restore values"
    length = xy.shape[0]
    xy = xy.transpose()
    r = np.empty((3, length))
    r[0] = 75
    r[1] = xy[0]
    r[2] = xy[1]
    return r.transpose()


def mean_shift(X):
    bandwidth = estimate_bandwidth(X, quantile=0.2, n_samples=1000)
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True, cluster_all=False)
    ms.fit(X)
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_
    return labels, cluster_centers


def dbscan(X):

    db = DBSCAN(eps=0.3, min_samples=10).fit(X)
    core_samples = db.core_sample_indices_
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    print n_clusters_
    return core_samples


def affinity(X):
    af = AffinityPropagation(preference=-50).fit(X)
    cluster_centers_indices = af.cluster_centers_indices_
    labels = af.labels_

    n_clusters_ = len(cluster_centers_indices)
    print cluster_centers_indices


def thresold(points, t=20):
    distances = distance.cdist(points, points)
    masks = distances < t
    lpoints = [(x, y) for x, y in points]
    a = set(lpoints)
    for i, mask in enumerate(masks):
        near = set([(x, y) for x, y in points[mask]])
        near.remove(lpoints[i])
        print len(near), points[i], near



if __name__ == "__main__":
    import sys

    X = convert(colors(sys.argv[1]))

    labels, cluster_centers = mean_shift(X[:,1:])
    print (labels).shape
    print cluster_centers.shape
    print "clusters", cluster_centers
    #thresold(cluster_centers)

    lab = unconvert(cluster_centers)
    print lab.shape
    rgbs = luv2rgb(lab.reshape((1, lab.shape[0], 3)))
    print rgbs

    with file('toto.html', 'w') as f:
        f.write('<html><body><table><tr>')
        for rgb in rgbs[0] * 256:
            color = [int(c) for c in rgb]
            f.write('<td style="background:rgb(%i, %i, %i); width:64px; height:64px;">&nbsp;</td>' % tuple(color))
        f.write('</tr></table><img src="%s"/></body></html>' % sys.argv[1])
