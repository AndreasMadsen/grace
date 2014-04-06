
import grace
import grace.times
import grace.ols
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

worldImage = mpimg.imread('equirectangular.png')

days = grace.ols.time_vector()
days_all = np.linspace(np.min(days), np.max(days), np.max(days) - np.min(days))
X_all = grace.ols.design_matrix(days_all, frequencies = 3, splines = True)
H = grace.ols.hat_matrix(X_all, frequencies = 3, splines = True)
description = grace.ols.theta_description(frequencies = 3, splines = True)

initial = (24, 134)

# The complexity in this code, comes from the clickability on the world map

def onclick(event):
	"""
	This is the function executed when the window is clicked on. The main purpose
	here is to filter invalid clicks and then call the redraw with the lat and
	lon index.
	"""
	if (event.xdata == None or event.ydata == None or event.button != 1 or
		event.xdata >= 360  or event.ydata >= 180 ): return

	redraw(int(event.ydata), int(event.xdata))

def histval(X):
	"""
	Computes histogram values for a data series. plt.hist was not used
	as this is not as updateable as just using plt.bars
	"""
	(frequencies, pos) = np.histogram(X, bins=np.arange(-3, 1, 0.05))
	return (frequencies, (pos[:-1] + pos[1:]) / 2)

# Create figure and attach mouse click handler
fig = plt.figure(figsize=(12, 9.3))
fig.canvas.mpl_connect('button_press_event', onclick)

# None of the code below plots anything (histogram is a funny exception)
# the purose is to initalize the window and then let redraw(lat, lon) do
# the actual data plotting.

# World map
plt.subplot(3,1,1)
plt.imshow(worldImage)
(point,) = plt.plot([], [], 'r*')
plt.ylim(179, 0)
plt.xlim(0, 359)
plt.xticks(np.arange(0, 360, 40), np.arange(-179.5, +179.5, 40))
plt.yticks(np.arange(0, 180, 20), np.arange(89.5, -89.5, -20))
plt.ylabel('latitude')
plt.xlabel('longitude')
plt.gca().xaxis.set_label_position('top')

# Scatter plot
plt.subplot(3,1,2)
(observe,) = plt.plot([], [], 'ro', label='Observations')
(estimat,) = plt.plot([], [], 'k-', label='Estimations')
plt.xlim(np.min(days), np.max(days))
date_ticks = np.linspace(np.min(days), np.max(days), 6).astype('int')
plt.xticks(date_ticks, grace.times.days_to_str(date_ticks))
plt.ylabel('EWH [m]')

# Histogram
plt.subplot(3,2,5)
(frequencies, pos) = histval(grace.grids[initial[0], initial[1], :])
hist_rects = plt.bar(pos, frequencies, pos[1] - pos[0], color='tomato')
plt.xlim(-3, 1)
plt.ylabel('frequency')
plt.xlabel('EWH [m]')

# Theta bars
plt.subplot(3,2,6)
theta_rects = plt.bar( np.arange(0, len(description)) + 0.5, np.zeros([len(description)]) )
plt.xlim(0, len(description) + 1)
plt.xticks(np.arange(1, len(description) + 1), description, fontsize = 9)
plt.setp(plt.xticks()[1], rotation=-90)

def redraw(latIndex, lonIndex):
	"""
	Sets the (x, y) data for the plots updates some
	axies and then redraw the window canvas.
	"""
	print (latIndex, lonIndex)

	# Get EWH values for this position
	Y = grace.grids[latIndex, lonIndex, :].ravel()
	Theta = grace.ols.theta_vector(Y)

	# Update star on world map
	plt.subplot(3,1,1)
	point.set_ydata([latIndex])
	point.set_xdata([lonIndex])

	# Update scatter plot
	plt.subplot(3,1,2)
	observe.set_ydata(Y)
	observe.set_xdata(days)

	estimat.set_ydata((H * np.asmatrix(Y).T).A.ravel())
	estimat.set_xdata(days_all)

	plt.ylim(np.min(Y)*1.2, np.max(Y)*1.2)

	# Update histogtam
	plt.subplot(3,2,5)
	(frequencies, pos) = histval(Y)
	for rect, f in zip(hist_rects, frequencies):
		rect.set_height(f)
	plt.ylim(0, np.max(frequencies) * 1.1)

	# Update histogtam
	plt.subplot(3,2,6)
	for rect, v in zip(theta_rects, Theta.A.ravel()):
		rect.set_height(v)
	plt.ylim(np.min(Theta)*1.2, np.max(Theta)*1.2)

	# Redraw window
	fig.canvas.draw()

# Do inital redraw also
redraw(initial[0], initial[1])

# Show window
plt.show()
