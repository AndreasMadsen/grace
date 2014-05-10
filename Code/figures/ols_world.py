# -*- coding: utf-8 -*-

from setup import *

import grace
import grace.ols
import os.path as path
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.basemap as maps

Theta = grace.ols.theta_matrix()
description = grace.ols.theta_description()

#
# Parameter plots
#

parameter_plots = [
	(1, 'vel', 'velocity $\\left[\\frac{m}{day}\\right]$'),
	(2, 'acc', 'acceleration $\\left[\\frac{m}{day^2}\\right]$')
];

for index, name, unit in parameter_plots:
	fig = plt.figure(figsize=(9, 3.5))

	m = maps.Basemap(projection='cyl', lon_0=0, resolution='c')
	m.drawcoastlines(linewidth=.5)
	m.drawparallels(np.arange(-90.,120.,30.),labels=[1,0,0,0])
	m.drawmeridians(np.arange(0.,420.,60.),labels=[0,0,0,1])
	im = m.imshow(Theta[::-1,:,index])
	im.set_cmap('binary_r')
	cbar = m.colorbar()
	cbar.set_label(unit, rotation=270, labelpad=20)

	fig.savefig(figure_path('ols-world-parameter-%s.pdf' % (name)))

execfile(path.join(basedir, 'ols_ih.py'), {}, {__name__: '__execfile__'})

fig = plt.gcf()
fig.set_size_inches(9, 3.5)
fig.savefig(figure_path('ols-world-parameter-year.pdf'))
