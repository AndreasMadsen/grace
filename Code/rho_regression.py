

import grace
import grace.ols
import grace.times

import scipy.optimize as optimize
import pandas
import numpy as np
import matplotlib.pyplot as plt

initial = (24, 134)

(y, days) = grace.ols.interpolate(initial[0], initial[1])
(y, X) = (np.asmatrix(y).T, grace.ols.design_matrix(grace.times.date_to_days(days)))

def inv_sigma_matrix(rho, size):
	offset_diag = -rho * np.ones((size-1,))
	middel_diag =  np.hstack([ 1, (1 + rho**2) * np.ones((size-2, )), 1 ])

	Sigma = np.diag(offset_diag, k=-1) + np.diag(offset_diag, k=1) + np.diag(middel_diag, k=0)
	return np.asmatrix(Sigma)

def sum_of_squares(params):
	rho = params[0]
	invSigma = inv_sigma_matrix(rho, y.size)
	beta = np.linalg.inv(X.T * invSigma * X) * X.T * invSigma * y
	return (y - X * beta).T * invSigma * (y - X * beta)

def residuals(rho):
	invSigma = inv_sigma_matrix(rho, y.size)
	beta = np.linalg.inv(X.T * invSigma * X) * X.T * invSigma * y
	return np.asarray(y - X * beta).ravel()

def rho_est(e):
	return np.sum(e[1:] * e[:-1]) / np.sum(e[1:-1]**2)

rho_new = 0
rho_old = 0
while True:
	rho_old = rho_new
	rho_new = rho_est(residuals(rho_new))
	if (rho_new >= 1 or rho_new <= -1):
		raise ValueError('rho eached %f' % (rho_new))
	if ((rho_new - rho_old)**2 <= 10e-6):
		break

print "Solution is:"
print "rho: %f " % rho_new
print "Sigma^2 using rho: %e" % (sum_of_squares([rho_new]) / (y.size - X.shape[1]))

error = np.asarray(y - grace.ols.hat_matrix(X, True) * y).ravel()
print "Sigma^2 normal: %e" % (np.sum(error**2) / (y.size - X.shape[1]))
