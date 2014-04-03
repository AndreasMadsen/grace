# -*- coding: utf-8 -*-

import grace
import grace.times
import grace.ols
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import mpl_toolkits.basemap as maps

# Load Thetas
description = grace.ols.theta_description()
Theta = grace.ols.theta_matrix()

#
# Plot phase as hue and amplitude as intensity
# choose an index of a cosine and let the following parameter be a 
# sine of equal frequence
# i.e. param=3: cos(2*pi/365*T) and sin(2*pi/365*T) will get
# an A and phi calculated
paramIndex = 3

amplitude = np.sqrt(Theta[:,:,paramIndex]**2 + Theta[:,:,paramIndex+1]**2)
phase = -np.arctan2(-Theta[:,:,paramIndex+1], Theta[:,:,paramIndex])

#
S = np.ones_like(amplitude)
v_1=S*np.cos(phase)
v_2=S*np.sin(phase)
#vektor=np.matrix([amplitude.ravel(),v_1.ravel(),v_2.ravel()])

#sanitty check:
vektor=np.matrix([np.ones_like(amplitude).ravel(),v_1.ravel(),v_2.ravel()])
a=-1/3.0
b=-1/np.sqrt(3)
c=1/np.sqrt(3)
d=2/3.0
IVV2RGB=np.matrix([[1, a,c],[1,a,d],[1,b,0]])
transformed=IVV2RGB*vektor
#HSV = np.dstack((phase[::-1,:],S,S))
RGB=np.asarray(transformed).reshape(
		3, 180, 360).transpose([1,2,0])
RGB=RGB[::-1,:]

fig = plt.figure(figsize=(12, 6))

m = maps.Basemap(projection='cyl', lon_0=0, resolution='c')
m.drawcoastlines(linewidth=.5)
m.drawparallels(np.arange(-90.,120.,30.), labels=[1,0,0,0])
m.drawmeridians(np.arange(0.,420.,60.), labels=[0,0,0,1])

#only plot the phase:
#im= m.imshow(phase[::-1], vmin=-np.pi, vmax=np.pi)

im = m.imshow(RGB, vmin=-np.pi, vmax=np.pi)
im.set_cmap('hsv')

# There is 12 month, split up [-pi, pi] intro 13 steps,
# where the first and last are the same
cbar = m.colorbar(ticks=np.linspace(-np.pi, np.pi, 13))
cbar.ax.set_yticklabels([
	"Juli",
	"August",
	"September",
	"Oktober",
	"November",
	"December",
	"Januar",
	"Februar",
	"Marts",
	"April",
	"Maj",
	"Juni",
	"Juli"
])

plt.title('Phase for: ' + description[paramIndex]+ ', '+description[paramIndex+1])

plt.show()
