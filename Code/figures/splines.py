# -*- coding: utf-8 -*-

from setup import *

import grace
import grace.ols
import os.path as path
import numpy as np
import matplotlib; backend = matplotlib.get_backend()
import matplotlib.pyplot as plt
import mpl_toolkits.basemap as maps

Theta = grace.ols.theta_matrix()
description = grace.ols.theta_description()
p_values = grace.ols.pvalue_matrix()

#
# Performance plots
#
print "Performance plots"

# Plot RMSE
execfile(path.join(basedir, 'splines_rmse.py'), {}, {__name__: '__execfile__'})

fig = plt.gcf()
fig.set_size_inches(9, 3.5)
fig.savefig(figure_path('splines-rmse.pdf'))

#
# Selected positions
#
positions = {
	"Greenland": (26, 130),
	"South Pole": (164, 92)
}

print "Selected positions are:"
for name in positions.keys():
	index = positions[name]
	coords = grace.positions[index[0], index[1]]
	print "  %10s: (%3.1f, %3.1f)" % (name, coords[0], coords[1])

#
#
# For each positon
#
#
days = grace.ols.time_vector()
days_all = np.linspace(np.min(days), np.max(days), np.max(days) - np.min(days))
H_all = grace.ols.hat_matrix(grace.ols.design_matrix(days_all, frequencies = 3, splines = True), frequencies = 3, splines = True)
H = grace.ols.hat_matrix(grace.ols.design_matrix(days, frequencies = 3, splines = True), frequencies = 3, splines = True)
description = grace.ols.theta_description(frequencies = 3, splines = True)

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
	fig.savefig(figure_path( "splines-selected-%d-fit.pdf" % (i) ))

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
	fig.savefig(figure_path( "splines-selected-%d-residual.pdf" % (i) ))
