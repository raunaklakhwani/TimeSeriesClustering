from sklearn.cluster import KMeans
import numpy


d = [(102, 209), (62, 75), (235, 151), (99, 221), (5, 207), (50, 176), (215, 267), (29, 183), (244, 266), (85, 224), (123, 175), (15, 165), (236, 205), (206, 100), (264, 160), (63, 95), (141, 45)]
ar = numpy.array(d)
for i in range(1, len(d) + 1):
    k = KMeans(n_clusters=10)
    k.fit(ar)
    print i, " ----> ", k.inertia_
