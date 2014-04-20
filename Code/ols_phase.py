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

# Calculate phase
phase = -np.arctan2(-Theta[:,:,paramIndex+1], Theta[:,:,paramIndex])

fig = plt.figure(figsize=(12, 6))

m = maps.Basemap(projection='cyl', lon_0=0, resolution='c')
m.drawcoastlines(linewidth=.5)
m.drawparallels(np.arange(-90.,120.,30.), labels=[1,0,0,0])
m.drawmeridians(np.arange(0.,420.,60.), labels=[0,0,0,1])

im = m.imshow(phase[::-1, :], vmin=-np.pi, vmax=np.pi)
im.set_cmap('hsv')

# There is 12 month, split up [-pi, pi] intro 13 steps,
# where the first and last are the same
cbar = m.colorbar(ticks=np.linspace(-np.pi, np.pi, 13))

### TODO: this lacks precision as it floors to the nearst month
###       , a diffrent implementation would be to offset the ticks
###       , thow there would stil be an issue with the first and
###       last tick.

# Get the epoch month (from 1 to 12)
epoch_month = grace.times.time_epoch.astype(datetime.date).month
months = [
	"Januar", "Februar", "Marts", "April", "Maj", "Juni",
	"Juli", "August", "September", "Oktober", "November", "December"
]

# First rool is so January appears in the middle (5 moves)
# Next rool is so epoch_month appears in the middle
ticks = np.roll(months, 5 - (epoch_month - 1))

# Make the last tick also appear in the begining
ticks = np.hstack((ticks[-1], ticks))

# Bind computed ticks to the color bar
cbar.ax.set_yticklabels( ticks )

plt.title('Phase for: ' + description[paramIndex]+ ', '+description[paramIndex+1])

plt.show()
