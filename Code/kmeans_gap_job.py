
import sklearn.cluster
from kmeans_gap import GAP
import grace
import grace.mask
import numpy as np
import sys

parallel = int(sys.argv[1] if (len(sys.argv) > 1) else 1)

if __name__=='__main__':
	shape = grace.grids.shape
	X = grace.grids.reshape(shape[0] * shape[1], shape[2])
	mask = grace.mask.world().reshape(shape[0] * shape[1])
	X = X[mask, :]

	optimizer = GAP(verbose=True)
	estimator = sklearn.cluster.KMeans(n_init=1, n_jobs=parallel)
	optimizer.calculate(X, estimator, sims=20, ks=range(1,21))

	np.savez('HPC-output/gap.npz', **optimizer.dump())

	(K, G, sd) = optimizer.optimal()
	print "Optimal amount of clusters: %d" % (K)
