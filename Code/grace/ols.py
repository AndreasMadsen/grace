# -*- coding: utf-8 -*-

import numpy as np
import times
import load
import pandas
import scipy.stats

EARTH_OMEGA = 365.242

def diag_pow(M, p):
	return np.diag(np.diag(M) ** p)

def splines_producer(X, t, factory, use_splines):
	if (use_splines):
		# Figure how many years there are
		t_year = times.days_to_date(t).astype('datetime64[Y]')

		# The -1 exists so the no spines are created for the last year,
		# this is because there aren't enogth observations to fit those
		# splines correctly.
		years = np.max(t_year) - np.min(t_year) - 1

		t_min = np.min(t)

		for s in range(0, years + 1):
			t_shift = t - EARTH_OMEGA * s
			t_transform = np.asarray(factory(t_shift)).T
			t_transform[t_shift < t_min, :] = 0

			X = np.column_stack( (X , t_transform) )
	else:
		X = np.column_stack( (X, np.asarray(factory(t)).T ) )

	return X

def splines_description(names, factory, use_splines):
	if (use_splines):
		# Figure how many years there are
		t_year = times.days_to_date(time_vector()).astype('datetime64[Y]')

		# The -1 exists so the no spines are created for the last year,
		# this is because there aren't enogth observations to fit those
		# splines correctly.
		years = np.max(t_year) - np.min(t_year) - 1

		for s in range(0, years + 1):
			names += factory('t - 365.2 * ' + str(s))
	else:
		names += factory('t')

	return names

def time_vector():
	"""
	Construct a time vector containg all the start dates
	as relative days since year 2000
	"""
	return times.date_to_days(load.dates[:,0])

def design_matrix(t=None, frequencies=18, splines=False):
	"""
	Construct the desgin matrix X from the time (t) as:
	[
		1, t, 0.5 * t^2,
		cos(2π/265.2 * t), sin(2π/265.2 * t),
		cos(2π/182.6 * t), sin(2π/182.6 * t),
		...,
		cos(2π/20.3 * t) , sin(2π/20.3 * t)
	]
	"""
	if (t is None): t = time_vector()

	# X = [1]
	X = np.ones((t.size, 1))

	# X = [t, 0.5 * t^2]
	X = splines_producer(X, t, lambda t: [t, 0.5 * (t**2)], use_splines=False)

	# X = [X, cos, sin, ...]
	# Max frequency is omega = 365.242 days per year. Samples come
	# every 10 days; 365/10 ~ 36. nyquist frequency 36/2 = 18
	for i in range(1, frequencies + 1):
		freq = (2 * np.pi)/(EARTH_OMEGA/i)
		X = splines_producer(X, t, lambda t: [ np.cos(freq * t), np.sin(freq * t) ], use_splines=splines)

	# Now that X is build, convert it to a matrix.
	# The matrix will symbolize a 37 dimentional space with 341 values
	return np.asmatrix(X)

def theta_description(frequencies=18, splines=False):
	"""
	Construct a simple array containg a description for all the
	theta values as strings.
	"""

	names = ["intercept (1)"]

	names = splines_description(names, lambda t: [
		"slope (" + t + ")",
		"acc. (0.5 * (" + t + ")^2)"
	], use_splines = False)

	omega = 365.242
	for i in range(1,frequencies + 1):
		names = splines_description(names, lambda t: [
			u"cos(2π/" + str(round(omega/i, 1)) +  " * (" + t + "))",
			u"sin(2π/" + str(round(omega/i, 1)) +  " * (" + t + "))"
		], use_splines = splines)

	return names

def theta_matrix(frequencies=18, splines=False):
	"""
	Construct a theta matrix (180, 360, p) containg all the theta vector
	for each world position
	"""
	X = design_matrix(frequencies=frequencies, splines=splines)

	# SVD factorize the X matrix, allowing for numerical stable calculation of
	# the hat matrix (H)
	U,S,V = np.linalg.svd(X, full_matrices=False)
	U,S,V = (U, np.diag(S), V.T)

	# Get the ewh values for all positions as a matrix. This matrix
	# will have the diffrent positons as collums and days on the rows
	shape = load.grids.shape
	Y = np.asmatrix(load.grids.reshape(shape[0] * shape[1], shape[2])).T

	# This will be a matrix of thetas as collums for each position.
	# The rows will be the theta parameters
	Theta = (V * diag_pow(S, -1) * U.T) * Y

	# Now reshape theta intro a (lat, lon, param) ndarray
	Theta = np.asarray(Theta).reshape(X.shape[1], shape[0], shape[1]).transpose([1,2,0])

	# All done
	return Theta

def pvalue_matrix(frequencies=18, splines=False):
	Theta = theta_matrix(frequencies=frequencies, splines=splines)
	H = hat_matrix(frequencies=frequencies, splines=splines)
	X = design_matrix(frequencies=frequencies, splines=splines)
	(n, p) = X.shape

	# SVD factorize the X matrix, allowing for numerical stable calculation of
	# the hat matrix (H)
	U,S,V = np.linalg.svd(X, full_matrices=False)
	U,S,V = (U, np.diag(S), V.T)

	# Get the ewh values for all positions as a matrix. This matrix
	# will have the diffrent positons as collums and days on the rows
	shape = load.grids.shape
	Y = np.asmatrix(load.grids.reshape(shape[0] * shape[1], shape[2])).T

	# Compute RMSR (sigma.hat)
	sigma = np.sqrt(np.sum(np.power(Y - H * Y, 2), 0) / (n - p))

	# Compute cov matrix without sigma^2 (makes it meaning full for all positions)
	S2inv = diag_pow(S, -2)
	cov_diag = np.asmatrix(np.diag(V * S2inv * V.T))

	# Compute a matrix of size(lat * lon, p) with sd(beta) values
	sd = np.sqrt(cov_diag.T) * sigma
	# Transform to (lat, lon, p)
	sd = np.asarray(sd).reshape(X.shape[1], shape[0], shape[1]).transpose([1,2,0])

	# Compute t-values, ndarray(lat, lon, p)
	t_values = Theta / sd

	# Compute p values
	prop = scipy.stats.t.cdf(t_values, n - p)
	return 2 * np.minimum(prop, 1 - prop)

def theta_vector(y, frequencies=18, splines=False):
	"""
	Contstruct a theta vector (p,) containg all the theta values for a
	a single given y vector
	"""
	X = design_matrix(frequencies=frequencies, splines=splines)

	# SVD factorize the X matrix, allowing for numerical stable calculation of
	# the hat matrix (H)
	U,S,V = np.linalg.svd(X, full_matrices=False)
	U,S,V = (U, np.diag(S), V.T)

	# This will be a matrix of thetas as collums for each position.
	# The rows will be the theta parameters
	Theta = (V * diag_pow(S, -1) * U.T) * np.asmatrix(y.ravel()).T

	return Theta

def pvalue_vector(y, frequencies=18, splines=False):
	y = np.asmatrix(y.ravel()).T

	Theta = theta_vector(y, frequencies=frequencies, splines=splines)
	H = hat_matrix(frequencies=frequencies, splines=splines)
	X = design_matrix(frequencies=frequencies, splines=splines)
	(n, p) = X.shape

	# SVD factorize the X matrix, allowing for numerical stable calculation of
	# the hat matrix (H)
	U,S,V = np.linalg.svd(X, full_matrices=False)
	U,S,V = (U, np.diag(S), V.T)

	# Compute RMSR (sigma.hat)
	sigma = float(np.sqrt(np.sum(np.power(y - H * y, 2), 0) / (n - p)))

	# Compute cov matrix without sigma^2 (makes it meaning full for all positions)
	S2inv = diag_pow(S, -2)
	cov_diag = np.diag(V * S2inv * V.T)

	# Compute a matrix of size(lat * lon, p) with sd(beta) values
	sd = np.sqrt(cov_diag) * sigma

	# Compute t-values, ndarray(lat, lon, p)
	t_values = Theta.A.ravel() / sd

	# Compute p values
	prop = scipy.stats.t.cdf(t_values, n - p)
	p = 2 * np.minimum(prop, 1 - prop)

	return p.ravel()

def hat_matrix(X=None, interpolate=False, frequencies=18, splines=False):
	"""
	Construct the hat matrix, there transforms y intro \hat{y}
	"""
	X_source = design_matrix(frequencies=frequencies, splines=splines)
	if (X is None): X = X_source
	if (interpolate is True): X_source = X

	# SVD factorize the X matrix, allowing for numerical stable calculation of
	# the hat matrix (H)
	U,S,V = np.linalg.svd(X_source, full_matrices=False)
	U,S,V = (U, np.diag(S), V.T)

	# Calculate hat matrix
	H = X * V * diag_pow(S, -1) * U.T

	# All done
	return H

def interpolate(latIndex, lonIndex):
	"""
	Interpolate the ewh and time values for some latIndex and lonIndex
	"""
	x = load.dates[:,0].ravel()
	y = load.grids[latIndex, lonIndex, :].ravel()

	# Bind the EWH data to the raw time values
	df = pandas.Series(y, index=x)

	# Generate time values from the start date (0,0)
	# to the end date(0,-1) with 10 days interval
	period = load.dates[0,0] + np.arange(0, (load.dates[-1,0] - load.dates[0,0]) + 10, 10, dtype='timedelta64[D]')

	# Reindex the time series, so it uses the interpolated dates,
	# there should now be quite a few missing values
	df = df.reindex(period)

	# Interpolate all missing values
	df = df.interpolate()

	# Return interpolated GLM constructs
	return (np.asarray(df), period)
