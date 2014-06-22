# -*- coding: utf-8 -*-

from setup import *

import grace
import grace.times
import grace.ols
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.basemap as maps

xx = np.array([-10, 10])
yy = np.array([-10, 10])
means = [xx.mean(), yy.mean()]
stds = [xx.std() / 3, yy.std() / 3]
corr = 0.9       # correlation
covs = [[stds[0]**2          , stds[0]*stds[1]*corr],
        [stds[0]*stds[1]*corr,           stds[1]**2]]

X = np.asmatrix(np.random.multivariate_normal(means, covs, 1000))

fig = plt.figure(figsize=(6,8))
plt.scatter(X[:, 0].A.ravel(), X[:, 1].A.ravel(), color="SteelBlue", alpha=0.7)
plt.ylim(-20, 20)
plt.xlim(-15, 15)
plt.gca().set_aspect('equal', adjustable='box')

#fig.savefig('original.pdf')

# Do SVD of residuals (transposed)
U,S,V = np.linalg.svd(X, full_matrices=False)
U,S,V = (U, np.diag(S), V.T)
print S
Z = X * V

fig = plt.figure(figsize=(6,8))

plt.scatter(Z[:, 0].A.ravel(), Z[:, 1].A.ravel(), color="SteelBlue", alpha=0.7)
plt.ylim(-20, 20)
plt.xlim(-15, 15)
plt.gca().set_aspect('equal', adjustable='box')

fig.savefig('rotated.pdf')

fig = plt.figure(figsize=(6,8))

plt.scatter(U[:, 0].A.ravel(), U[:, 1].A.ravel(), color="SteelBlue", alpha=0.7)
plt.ylim(-0.20, 0.20)
plt.xlim(-0.15, 0.15)
plt.gca().set_aspect('equal', adjustable='box')

#fig.savefig('scaled.pdf')

plt.show()
