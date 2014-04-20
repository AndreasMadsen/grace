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

hsv = np.zeros((150, 360, 3))
for h in range(0, 360):
	for v in range(0, 150):
		hsv[v, h, :] = [
			(float(h) / 360.0) * (2.0 * np.pi) - np.pi,
			1,
			float(v) / 100.0
		]

print "H range: %f to %f " % (np.min(hsv[:,:,0]), np.max(hsv[:,:,0]))
print "S range: %f to %f " % (np.min(hsv[:,:,1]), np.max(hsv[:,:,1]))
print "V range: %f to %f " % (np.min(hsv[:,:,2]), np.max(hsv[:,:,2]))

rgb = colors.hsv_to_rgb(hsv)

im = plt.imshow(rgb)

plt.show()
