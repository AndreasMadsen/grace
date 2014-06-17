
import sklearn.cluster
from kmeans_gap import GAP
import grace
import grace.mask
import numpy as np

if __name__=='__main__':
	shape = grace.grids.shape
	X = grace.grids.reshape(shape[0] * shape[1], shape[2])
	mask = grace.mask.mask_matrix().reshape(shape[0] * shape[1])
	X = X[mask, :]

	optimizer = GAP(verbose=True)
	estimator = sklearn.cluster.KMeans(n_clusters=8, n_jobs=-1)
	optimizer.calculate(X, estimator, sims=3, ks=range(1,10))

	np.savez('HPC-output/gap.npz', **optimizer.dump())
