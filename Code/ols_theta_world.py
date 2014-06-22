# -*- coding: utf-8 -*-

import grace
import grace.times
import grace.ols
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.basemap as maps

# Construct the Theta matrix (lat, lon, p)
Theta = grace.ols.theta_matrix()
# Get the description for the Theta values
description = grace.ols.theta_description()

#
# Plot Theta parameter for all positions
#
paramIndex = 1

fig = plt.figure(figsize=(12, 6))

m = maps.Basemap(projection='cyl', lon_0=0, resolution='c')
m.drawcoastlines(linewidth=.5)
m.drawparallels(np.arange(-90.,120.,30.),labels=[1,0,0,0])
m.drawmeridians(np.arange(0.,420.,60.),labels=[0,0,0,1])

im = m.imshow(Theta[::-1,:,paramIndex])
im.set_cmap('binary_r')

m.colorbar()

plt.title(description[paramIndex])

plt.show()
