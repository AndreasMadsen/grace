
import grace
import grace.mask
import grace.times
import grace.ols
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.basemap as maps

import sklearn.mixture
import sklearn.decomposition

# Transform grids data
shape = grace.grids.shape
X = grace.grids.reshape(shape[0] * shape[1], shape[2])
mask = grace.mask.mask_matrix()
X = X[mask.reshape(shape[0] * shape[1]), :]

pca = sklearn.decomposition.KernelPCA(kernel='rbf', fit_inverse_transform=True)
X = pca.fit_transform(X)

#
# Variance explaned
#
np.save('HPC-output/pca_kernel_lambda.npy', pca.lambdas_)
