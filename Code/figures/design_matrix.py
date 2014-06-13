# -*- coding: utf-8 -*-

from setup import *

import grace
import grace.ols
import numpy as np
import os.path as path
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

(latIndex, lonIndex) = (26, 130)

#
#
# For each positon
#
#
Y = np.asmatrix(grace.grids[latIndex, lonIndex, :]).T
days = grace.ols.time_vector()
days_all = np.linspace(np.min(days), np.max(days), np.max(days) - np.min(days))

def diag_pow(M, p):
	return np.diag(np.diag(M) ** p)

def estimate(producer):
	# SVD factorize the X matrix, allowing for numerical stable calculation of
	# the hat matrix (H)
	U,S,V = np.linalg.svd(np.asmatrix(producer(days)), full_matrices=False)
	U,S,V = (U, np.diag(S), V.T)

	# This will be a matrix of thetas as collums for each position.
	# The rows will be the theta parameters
	Theta = (V * diag_pow(S, -1) * U.T) * np.asmatrix(Y.A.ravel()).T
	print Theta.shape
	return np.asmatrix(producer(days_all)) * Theta

def genplot(name, producer):
	#
	# Plot y and y.hat
	#
	fig = plt.figure(figsize=(10, 4))
	plt.scatter(days, Y.A.ravel(), color="SteelBlue", alpha=0.7)
	plt.plot(days_all, estimate(producer).A.ravel(), color="IndianRed")

	# Setup ticks
	date_ticks = np.linspace(np.min(days), np.max(days), 6).astype('int')
	plt.xticks(date_ticks, grace.times.days_to_str(date_ticks))
	plt.xlim(np.min(days), np.max(days))
	plt.ylabel('EWH [m]')
	fig.savefig('%s.pdf' % (name))

genplot('velocity'    , lambda t: np.column_stack([ np.ones((t.size, 1)), t              ]) )
genplot('acceleration', lambda t: np.column_stack([ np.ones((t.size, 1)), t, 0.5 * (t**2)]) )
genplot('yearly'      , lambda t: grace.ols.design_matrix(t, frequencies=1)                 )
genplot('full'        , lambda t: grace.ols.design_matrix(t, frequencies=18)                )
