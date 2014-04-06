# -*- coding: utf-8 -*-

import grace
import grace.times
import grace.ols
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import mpl_toolkits.basemap as maps

# Load Thetas
description = grace.ols.theta_description()
Theta = grace.ols.theta_matrix()

# Parameter index for cos term
paramIndex = 3

# Calculate amplitude
amplitude = np.sqrt(Theta[:,:,paramIndex]**2 + Theta[:,:,paramIndex+1]**2)

fig = plt.figure(figsize=(12, 6))

m = maps.Basemap(projection='cyl', lon_0=0, resolution='c')
m.drawcoastlines(linewidth=.5)
m.drawparallels(np.arange(-90.,120.,30.), labels=[1,0,0,0])
m.drawmeridians(np.arange(0.,420.,60.), labels=[0,0,0,1])

im = m.imshow(amplitude[::-1, :], vmin=0)
im.set_cmap('binary_r')

m.colorbar()

plt.title('Amplitude for: ' + description[paramIndex]+ ', '+description[paramIndex+1])

plt.show()
