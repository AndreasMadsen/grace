# -*- coding: utf-8 -*-

import grace
import grace.ols
import grace.gia
import grace.mask
import numpy as np

(lons, lats) = (grace.positions[:, :, 1], grace.positions[:, :, 0])
EARTH_RADIUS = 6371.0 # km

#
# Calculate GIA velocity
#
velocity = grace.ols.theta_matrix()[:, :, 1]
data = (velocity - grace.gia.grid)

#
# Calculate area for all locations
#
def area_kernel(lon, lat):
	"""
		lat and lon have a 1 degree interval
	"""
	lat1 = (lat - 0.5) * (np.pi / 180.0)
	lat2 = (lat + 0.5) * (np.pi / 180.0)
	return (np.pi/180.0) * (EARTH_RADIUS**2) * np.abs(np.sin(lat1)-np.sin(lat2)) * 1

area = np.vectorize(area_kernel)
area_map = area(lons, lats)

#
# Mask velocity and area
#
mask = grace.mask.greenland().reshape((180 * 360))
greenland_area = area_map.reshape((180 * 360))[mask]
greanland_vel = velocity.reshape((180 * 360))[mask]

