# -*- coding: utf-8 -*-

import grace
import grace.times
import grace.ols
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.basemap as maps

# Compute the hat matrix
days = grace.ols.time_vector()
H = grace.ols.hat_matrix()
p = len(grace.ols.theta_description())

# Get the ewh values for all positions as a matrix. This matrix
# will have the diffrent positons as collums and days on the rows
shape = grace.grids.shape
Y = np.asmatrix(grace.grids.reshape(shape[0] * shape[1], shape[2])).T

# Compute RMSR
RMSR = np.sqrt(np.sum(np.power(Y - H * Y, 2), 0) / (days.size - p))
RMSR = RMSR.reshape(180, 360)

#
# Plot Theta parameter for all positions
#
fig = plt.figure(figsize=(12, 6))

m = maps.Basemap(projection='cyl', lon_0=0, resolution='c')
m.drawcoastlines(linewidth=.5)
m.drawparallels(np.arange(-90.,120.,30.),labels=[1,0,0,0])
m.drawmeridians(np.arange(0.,420.,60.),labels=[0,0,0,1])

im = m.imshow(RMSR[::-1,:])
im.set_cmap('binary_r')

m.colorbar()

if (__name__ == '__main__'): plt.show()
