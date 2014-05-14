# -*- coding: utf-8 -*-

from setup import *

import grace
import grace.ols
import os.path as path
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.basemap as maps

H = grace.ols.hat_matrix()
days = grace.ols.time_vector()

#
# Compute the U tensor
#

# Get the ewh values for all positions as a matrix. This matrix
# will have the diffrent positons as collums and days on the rows
shape = grace.grids.shape
Y = np.asmatrix(grace.grids.reshape(shape[0] * shape[1], shape[2])).T

# Calculate residuals (collums: position, rows: days)
e = Y - H * Y

# Do SVD of residuals (transposed)
U,S,V = np.linalg.svd(e.T, full_matrices=False)
U,S,V = (U, np.diag(S), V.T)

# Transform U intro a (lat, lon, day) ndarray
U_grid = np.asarray(U.T).reshape(shape[2], shape[0], shape[1]).transpose([1,2,0])

#
# Generate variance explained plot
#
fig = plt.figure(figsize=(10, 4))

S_diag = np.diag(S)
rho = (S_diag**2) / (S_diag**2).sum()

plt.bar(range(0, rho.shape[0]), rho * 100, color='SteelBlue')

plt.xlim(0, rho.shape[0] / 3)
plt.xlabel('Principal component')
plt.ylabel('%')
plt.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.15)

fig.savefig(figure_path('ols-pca-explained.pdf'))

for pc in [0, 1]:
	#
	# Plot Principal Component scores
	#
	fig = plt.figure(figsize=(9, 3.5))

	m = maps.Basemap(projection='cyl', lon_0=0, resolution='c')
	m.drawcoastlines(linewidth=.5)
	m.drawparallels(np.arange(-90.,120.,30.), labels=[1,0,0,0])
	m.drawmeridians(np.arange(0.,420.,60.), labels=[0,0,0,1])
	im = m.imshow(U_grid[::-1,:,pc])
	im.set_cmap('binary_r')
	m.colorbar()

	fig.savefig(figure_path('ols-pca-score-%d.pdf' % (pc)))

	#
	# Plot Principal Compoent loadings
	#
	fig = plt.figure(figsize=(10, 4))

	years_split = grace.times.date_to_days(
		np.unique(
			grace.times.days_to_date(days).astype('datetime64[Y]')
		).astype('datetime64[D]')[1:]
	)

	plt.plot(days, V[:, pc].A.ravel(), color="SteelBlue")
	plt.ylim(*plt.ylim())
	plt.vlines(years_split, *plt.ylim(), color='Gray', linestyles='dotted')

	plt.xticks(years_split[::2], grace.times.days_to_str(years_split[::2]))
	plt.xlim(np.min(days), np.max(days))

	print figure_path('ols-pca-loading-%d.pdf' % (pc))
	fig.savefig(figure_path('ols-pca-loading-%d.pdf' % (pc)))
