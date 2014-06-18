
import sklearn.cluster
from kmeans_gap import GAP
import grace
import grace.mask
import grace.times
import grace.ols
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.basemap as maps

# Color map for cluster index
colors_hex = [
	"a6cee3", "1f78b4", "b2df8a", "33a02c", "fb9a99", "e31a1c",
	"fdbf6f", "ff7f00", "cab2d6", "6a3d9a", "ffff99", "b15928"
]
colors_rgb = map(lambda hex: [ord(c) for c in hex.decode('hex')], colors_hex)

#
# Plot GAP statistics
#
plt.figure(figsize=(8,4.2))

optimizer = GAP(verbose=True)
optimizer.load(np.load('HPC-output/gap.npz'))

(K, G, sd) = optimizer.optimal()
print "Optimal amount of clusters: %d" % (K)
if (K > 12):
	print "WARNING: Current only 12 clusters are supported (colors)"
	K = 12
plt.errorbar(optimizer.ks, G, sd)
plt.xlim(optimizer.ks[0], optimizer.ks[-1])

#
# Plot World
#
plt.figure(figsize=(9, 3.5))

# Transform grids data
shape = grace.grids.shape
X = grace.grids.reshape(shape[0] * shape[1], shape[2])
mask = grace.mask.mask_matrix()
X = X[mask.reshape(shape[0] * shape[1]), :]

# Perform clustering
estimator = sklearn.cluster.KMeans(n_clusters=K)
groups = estimator.fit_predict(X)
print "Cluster calculation done"

# Build color coded world matrix
world = np.ones((shape[0], shape[1], 3)).astype('uint8') * 255

p = 0
for i in range(0, shape[0]):
	for j in range(0, shape[1]):
		if (mask[i, j]):
			world[i, j, :] = colors_rgb[groups[p]]
			p += 1

m = maps.Basemap(projection='cyl', lon_0=0, resolution='c')
m.drawcoastlines(linewidth=.5)
m.drawparallels(np.arange(-90.,120.,30.), labels=[1,0,0,0])
m.drawmeridians(np.arange(0.,420.,60.), labels=[0,0,0,1])
m.imshow(world[::-1, :, :], interpolation="bicubic")

#
# Plot Centroids
#
plt.figure(figsize=(8,4.2))

centroids = estimator.cluster_centers_
days = grace.ols.time_vector()

for i in range(0, centroids.shape[0]):
	plt.plot(days, centroids[i, :].ravel(), '-', color='#' + colors_hex[i])

plt.ylim(*plt.ylim())

years_split = grace.times.date_to_days(
	np.unique(
		grace.times.days_to_date(days).astype('datetime64[Y]')
	).astype('datetime64[D]')[1:]
)

plt.vlines(years_split, *plt.ylim(), color='Gray', linestyles='dotted')
plt.xticks(years_split[::2], grace.times.days_to_str(years_split[::2]))
plt.xlim(np.min(days), np.max(days))

plt.show()
