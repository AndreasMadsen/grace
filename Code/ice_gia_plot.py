# -*- coding: utf-8 -*-

import grace
import grace.gia
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.basemap as maps

#
# Plot Theta parameter for all positions
#
data = grace.gia.grid * 3600
minmax = {"vmin": -0.26, "vmax": 0.10}


fig = plt.figure(figsize=(12, 4.5))

#
# Do the north pole
#
plt.subplot(1,2,1)
plt.title('North Pole')

m = maps.Basemap(projection='npstere', lon_0=270, boundinglat=10, resolution='c')
m.drawcoastlines(linewidth=.5)
m.drawparallels(np.arange(-90.,120.,30.))
m.drawmeridians(np.arange(0.,420.,60.))

im = m.pcolor(grace.gia.lons, grace.gia.lats, data, latlon=True, **minmax)
im.set_cmap('binary_r')

#
# Do the south pole
#
plt.subplot(1,2,2)
plt.title('South Pole')

m = maps.Basemap(projection='spstere', lon_0=90, boundinglat=-10, resolution='c')
m.drawcoastlines(linewidth=.5)
m.drawparallels(np.arange(-90.,120.,30.))
m.drawmeridians(np.arange(0.,420.,60.))

im = m.pcolor(grace.gia.lons, grace.gia.lats, data, latlon=True, **minmax)
im.set_cmap('binary_r')

#
# Make colorbar
#

fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.20, 0.03, 0.6])
cbar = fig.colorbar(im, cax=cbar_ax)
cbar.set_label('$\\left[\\frac{m}{year}\\right]$', rotation=270, labelpad=20)

fig.savefig('../Rapport/figures/gia-pure-adjust.png', dpi=310)
