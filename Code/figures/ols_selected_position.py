# -*- coding: utf-8 -*-

from setup import *

import grace
import grace.ols
import numpy as np
import os.path as path
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from tabulate import tabulate
import re

positions = {
	"Greenland": (26, 130),
	"South Pole": (164, 92)
}

print "Selected positions are:"
for name in positions.keys():
	index = positions[name]
	coords = grace.positions[index[0], index[1]]
	print "  %10s: (%3.1f, %3.1f)" % (name, coords[0], coords[1])

worldImage = mpimg.imread(path.join(basedir, 'equirectangular.png'))

#
# Show selected positions on a world map
#
fig = plt.figure(figsize=(8,4.2))
plt.imshow(worldImage)
plt.plot(
	[positions[name][1] for name in positions.keys()],
	[positions[name][0] for name in positions.keys()],
	'r*'
)

plt.ylim(179, 0)
plt.xlim(0, 359)
plt.xticks(np.arange(0, 360, 40), np.arange(-179.5, +179.5, 40))
plt.yticks(np.arange(0, 180, 20), np.arange(89.5, -89.5, -20))

plt.ylabel('latitude')
plt.xlabel('longitude')
fig.savefig(figure_path("ols-selected-map.pdf"))

#
#
# For each positon
#
#
days = grace.ols.time_vector()
days_all = np.linspace(np.min(days), np.max(days), np.max(days) - np.min(days))
H_all = grace.ols.hat_matrix(grace.ols.design_matrix(days_all))
H = grace.ols.hat_matrix(grace.ols.design_matrix(days))
description = grace.ols.theta_description()

(n, p) = (days.shape[0], len(description))

for i, name in enumerate(positions.keys()):
	print "\n\n%s" % (name)

	(latIndex, lonIndex) = positions[name]
	coords = grace.positions[latIndex, lonIndex]
	Y = np.asmatrix(grace.grids[latIndex, lonIndex, :]).T

	#
	# Plot y and y.hat
	#
	fig = plt.figure(figsize=(10, 4))
	plt.scatter(days, Y.A.ravel(), color="SteelBlue", alpha=0.7)
	plt.plot(days_all, (H_all * Y).A.ravel(), color="IndianRed")

	# Setup ticks
	date_ticks = np.linspace(np.min(days), np.max(days), 6).astype('int')
	plt.xticks(date_ticks, grace.times.days_to_str(date_ticks))
	plt.xlim(np.min(days), np.max(days))
	plt.ylabel('EWH [m]')
	fig.savefig(figure_path( "ols-selected-%d-fit.pdf" % (i) ))

	#
	# Plot residuals
	#
	fig = plt.figure(figsize=(10, 4))
	plt.plot(days, (Y - H * Y).A.ravel(), color="SteelBlue", alpha=0.7)
	plt.axhline(0, np.min(days), np.max(days), color='Gray')

	# Setup ticks
	date_ticks = np.linspace(np.min(days), np.max(days), 6).astype('int')
	plt.xticks(date_ticks, grace.times.days_to_str(date_ticks))
	plt.xlim(np.min(days), np.max(days))
	plt.ylabel('Residuals [m]')
	fig.savefig(figure_path( "ols-selected-%d-residual.pdf" % (i) ))

	#
	# Print RMSE
	#
	rmse = np.sum( np.power((Y - H * Y).A.ravel(), 2) ) / (len(days) - p)
	print "RMSE: %s" % (rmse)

	#
	# Print theta and p values
	#
	theta = grace.ols.theta_vector(Y.A.ravel()).A.ravel()
	pvalues = grace.ols.pvalue_vector(Y.A.ravel())

	tabel_content = []
	for index, name in enumerate(description):
		tabel_content.append([
			'$' + latexity(name).replace('frac', 'sfrac').replace('vel. t', 'vel. (t)') + '$',
			'$' + latexity('%.2e' % (theta[index])) + '$',
			'$%.3f$' % (pvalues[index])
		])
	tabel_content.append(['', '', ''])

	with open(figure_path('ols-selected-%d-paramters.tex' % (i)), "w") as texfile:
	    texfile.write(
			tabulate(tabel_content[:20], headers=["name","estimate", "p-value"], tablefmt="latex").replace('lll', 'r|rr')
	    )
	    texfile.write('\\hspace{1cm}')
	    texfile.write(
			tabulate(tabel_content[20:], headers=["name","estimate", "p-value"], tablefmt="latex").replace('lll', 'r|rr')
	    )

#plt.show()
