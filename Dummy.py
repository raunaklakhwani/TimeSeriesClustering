from sklearn import datasets
import numpy
from sklearn.cluster import KMeans

data = numpy.array([[1,2],[3,4],[1,5],[2,9],[13,14],[23,21],[21,23],[4,4],[10,10]])

kmeans = KMeans(n_clusters=5,init='k-means++')
kmeans.fit(data)

import numpy as np
import matplotlib.pyplot as plt


x = [row[0] for row in data]
y = [row[1] for row in data]
N = 50

colors = np.random.rand(N)
area = np.pi * (15 * np.random.rand(N))**2 # 0 to 15 point radiuses

plt.scatter(x, y, c=kmeans.labels_, alpha=0.5)
plt.show()
