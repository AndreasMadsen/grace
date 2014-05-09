# -*- coding: utf-8 -*-

from setup import *

import grace
import grace.times
import grace.ols
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.basemap as maps

initial = (26, 130)

#
# Generate a world figure
#
date = 230

fig = plt.figure(figsize=(8, 3.5))

m = maps.Basemap(projection='cyl', lon_0=0, resolution='c')
m.drawcoastlines(linewidth=.5)
m.drawparallels(np.arange(-90.,120.,30.),labels=[1,0,0,0])
m.drawmeridians(np.arange(0.,420.,60.),labels=[0,0,0,1])

im = m.imshow(grace.grids[::-1,:,date])
im.set_cmap('binary_r')

cbar = m.colorbar()
cbar.set_label('EMH [m]', rotation=270, labelpad=20)

plt.title("EWH [m] - " + str(grace.dates[date,0]))

fig.savefig(figure_path("data-example-world.eps"))

#
# Generate a scatter plot
#
fig = plt.figure(figsize=(10, 4))

Y = np.asmatrix(grace.grids[initial[0], initial[1], :]).T
days = grace.ols.time_vector()

# Plot y and y.hat
plt.scatter(days, Y.A.ravel(), color="SteelBlue", alpha=0.7)

date_ticks = np.linspace(np.min(days), np.max(days), 6).astype('int')
plt.xticks(date_ticks, grace.times.days_to_str(date_ticks))
plt.xlim(np.min(days), np.max(days))

plt.ylabel('EWH [m]')
plt.title("%.1f N, %.1f W" % tuple( np.abs(grace.positions[initial[0], initial[1]]) ))
fig.savefig(figure_path("data-example-scatter.pdf"))
