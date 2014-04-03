# -*- coding: utf-8 -*-

import grace
import grace.times
import grace.ols
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.basemap as maps
from scipy.stats import t

# Compute the hat matrix
description = grace.ols.theta_description()
Theta = grace.ols.theta_matrix()
days = grace.ols.time_vector()
X = grace.ols.design_matrix()
H = grace.ols.hat_matrix()
p = len(description)

# SVD factorize the X matrix, allowing for numerical stable calculation of
# the hat matrix (H)
U,S,V = np.linalg.svd(X, full_matrices=False)
U,S,V = (U, np.diag(S), V.T)

# Get the ewh values for all positions as a matrix. This matrix
# will have the diffrent positons as collums and days on the rows
shape = grace.grids.shape
Y = np.asmatrix(grace.grids.reshape(shape[0] * shape[1], shape[2])).T

# Compute RMSR (sigma.hat)
sigma = np.sqrt(np.sum(np.power(Y - H * Y, 2), 0) / (days.size - p))

# Compute cov matrix without sigma^2 (makes it meaning full for all positions)
S2inv = np.linalg.inv(S * S)
cov_diag = np.asmatrix(np.diag(V * S2inv * V.T))

# Compute a matrix of size(lat * lon, p) with sd(beta) values
sd = np.sqrt(cov_diag.T) * sigma
# Transform to (lat, lon, p)
sd = np.asarray(sd).reshape(X.shape[1], shape[0], shape[1]).transpose([1,2,0])

# Compute t-values, ndarray(lat, lon, p)
t_values = Theta / sd

# Compute p values
prop = t.cdf(t_values, days.size - p)
p_values = 2 * np.minimum(prop, 1 - prop)

#
# Plot Theta parameter for all positions
#
paramIndex = 2

fig = plt.figure(figsize=(12, 6))

m = maps.Basemap(projection='cyl', lon_0=0, resolution='c')
m.drawcoastlines(linewidth=.5, color="white")
m.drawparallels(np.arange(-90.,120.,30.), labels=[1,0,0,0])
m.drawmeridians(np.arange(0.,420.,60.), labels=[0,0,0,1])

im = m.imshow(p_values[::-1,:,paramIndex], vmin=0, vmax=1)
im.set_cmap('binary_r')

m.colorbar()

plt.title(description[paramIndex])

plt.show()
