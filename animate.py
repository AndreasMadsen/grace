
import grace
import math
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.basemap as maps
import matplotlib.animation as animation

fig = plt.figure(figsize=(12, 6))

m = maps.Basemap(projection='cyl', lon_0=0, resolution='c')
m.drawcoastlines(linewidth=.5)
m.drawparallels(np.arange(-90.,120.,30.),labels=[1,0,0,0])
m.drawmeridians(np.arange(0.,420.,60.),labels=[0,0,0,1])

im = m.imshow(grace.grids[::-1,:,0], vmax=math.ceil(np.max(grace.grids)), vmin=math.floor(np.min(grace.grids)))
im.set_cmap('binary_r')

print grace.grids[::-1,:,:].shape

def updatefig(period):
	im.set_data(grace.grids[::-1,:,period])
	plt.title(str(grace.dates[period, 0]))

ani = animation.FuncAnimation(fig, updatefig, frames=grace.grids.shape[2], interval=20, blit=False, repeat=False)

m.colorbar()

plt.show()
