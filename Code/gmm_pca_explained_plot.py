
import grace
import grace.mask
import grace.times
import grace.ols
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.basemap as maps

import sklearn.mixture
import sklearn.decomposition

lambdas = np.load('HPC-output/pca_kernel_lambda.npy')
print lambdas.shape

fig = plt.figure(figsize=(10, 4))

rho = (lambdas) / (lambdas).sum()
print "Variance explaned by first 10 PCs %f" % (rho[0:10].sum())
rho = rho[0:25]
plt.bar(range(0, rho.shape[0]), rho * 100, color='SteelBlue')

plt.xlim(0, rho.shape[0])
plt.xlabel('Principal component')
plt.ylabel('%')
plt.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.15)

fig.savefig('../Rapport/figures/gmm-pca-explaned.pdf')
