

import grace
import grace.ols
import grace.times

import scipy.optimize as optimize
import pandas
import numpy as np
import matplotlib.pyplot as plt

initial = (24, 134)

def interpolate(latIndex, lonIndex): 
	x = grace.dates[:,0].ravel()
	y = grace.grids[latIndex, lonIndex, :].ravel()

	# Bind the EWH data to the raw time values
	df = pandas.Series(y, index=x)

	# Generate time values from the start date (0,0)
	# to the end date(0,-1) with 10 days interval
	period = grace.dates[0,0] + np.arange(0, (grace.dates[-1,0] - grace.dates[0,0]) + 10, 10, dtype='timedelta64[D]')

	# Reindex the time series, so it uses the interpolated dates,
	# there should now be quite a few missing values
	df = df.reindex(period)

	# Interpolate all missing values
	df = df.interpolate()

	# Create design matrix
	X = grace.ols.design_matrix(grace.times.date_to_days(period))

	# Return interpolated GLM constructs
	return (X, np.asmatrix(np.asarray(df)).T, period)

(X, y, days) = interpolate(initial[0], initial[1])

np.savetxt("ts_greenland.csv", y.A.ravel(), delimiter=",")
