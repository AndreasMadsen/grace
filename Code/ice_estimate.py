# -*- coding: utf-8 -*-

import grace
import grace.ols
import grace.gia
import grace.mask
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate

(lons, lats) = (grace.positions[:, :, 1], grace.positions[:, :, 0])
EARTH_RADIUS = 6371000.0 # m

#
# Calculate GIA velocity
#
theta = grace.ols.theta_matrix()
velocity = theta[:, :, 1]
acceleration = theta[:, :, 2]
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
greenland_area = area_map.reshape((180 * 360))[mask] # m^2
greanland_vel = velocity.reshape((180 * 360))[mask] # m
greanland_acc = acceleration.reshape((180 * 360))[mask] # m

ewh = lambda t: np.sum(greenland_area * (greanland_vel * t + 0.5 * greanland_acc * t**2) * 997.0) # kg

days = grace.ols.time_vector()
years = np.unique(grace.times.days_to_date(days).astype('datetime64[Y]'))
years_str = years.astype('str')
years_days = grace.times.date_to_days(years.astype('datetime64[D]'))

for i in range(0, years.shape[0] - 1):
	loss = ewh(years_days[i]) - ewh(years_days[i + 1])

	print "From %s to %s, mass loss was %f giga ton" % (years_str[i], years_str[i + 1], loss / (10**12))

