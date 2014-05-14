

import grace
import grace.ols
import grace.times

import scipy.optimize as optimize
import pandas
import scipy as sp
import numpy as np
import matplotlib.pyplot as plt

initial = (26, 130)

y_plain = np.asmatrix(grace.grids[initial[0], initial[1], :]).T
days_plain = grace.ols.time_vector()
(y_plain, X_plain) = (np.asmatrix(y_plain).T, grace.ols.design_matrix(days_plain))

(y, days) = grace.ols.interpolate(initial[0], initial[1])
days = grace.times.date_to_days(days)
(y, X) = (np.asmatrix(y).T, grace.ols.design_matrix(days))

def inv_sigma_matrix(rho, size):
	offset_diag = -rho * np.ones((size-1,))
	middel_diag =  np.hstack([ 1, (1 + rho**2) * np.ones((size-2, )), 1 ])

	Sigma = np.diag(offset_diag, k=-1) + np.diag(offset_diag, k=1) + np.diag(middel_diag, k=0)
	return np.asmatrix(Sigma)

def estimate_beta(rho):
	invSigma = inv_sigma_matrix(rho, y.size)
	return np.linalg.inv(X.T * invSigma * X) * X.T * invSigma * y

def estimate_rho(beta):
	residuals = np.asarray(y - X * beta).ravel()
	return np.sum(residuals[1:] * residuals[:-1]) / np.sum(residuals[1:-1]**2)

def sum_of_squares(rho, beta):
	invSigma = inv_sigma_matrix(rho, y.size)
	return float((y - X * beta).T * invSigma * (y - X * beta))

def durbin_watson(rho, beta):
	invSigma = inv_sigma_matrix(rho, y.size)
	residuals = sp.linalg.sqrtm(invSigma) * (y - X * beta)
	residuals = residuals.A.ravel()
	return np.sum(np.diff(residuals)**2) / np.sum(residuals**2)

def optimize():
	rho_last = 0
	rho = 0

	iteration = 0
	while True:
		rho_last = rho
		iteration += 1

		# Estimate parameters
		beta = estimate_beta(rho)
		rho = estimate_rho(beta)

		# Check rho bound
		if (rho >= 1 or rho <= -1):
			raise ValueError('rho out of bound: %f' % (rho_new))
		# Convergence
		if ((rho - rho_last)**2 <= 10e-10):
			break
		# Max iteration
		if (iteration >= 1000):
			break

	# Done optimizing return result
	return (beta, rho)

(beta, rho) = optimize()

#
# Summary
#

print "Solution is:"
print "rho: %f " % rho
print "Sigma^2 using rho: %e" % (sum_of_squares(rho, beta) / (y.size - X.shape[1]))
print "durbin-watson: %f" % (durbin_watson(rho, beta))
error = np.asarray(y_plain - X_plain * beta).ravel()
print "MSR: %f" % (np.sum(error**2) / (y_plain.size - X_plain.shape[1]))


print "\nCompare with:"
plain_beta = grace.ols.theta_vector(y_plain.A.ravel())
plain_error = np.asarray(y_plain - X_plain * plain_beta).ravel()
print "Sigma^2 normal: %e" % (sum_of_squares(0, plain_beta) / (y.size - X.shape[1]))
print "durbin-watson: %f" % (durbin_watson(0, plain_beta))
print "MSR: %f" % (np.sum(plain_error**2) / (y_plain.size - X_plain.shape[1]))

#
#
#

fig = plt.figure(figsize=(10, 6))

# Plot y and y.hat
plt.scatter(days_plain, y_plain.A.ravel(), color="SteelBlue", alpha=0.7)
plt.plot(days, (X * plain_beta).A.ravel(), '-', color = 'black', label='OLS')
plt.plot(days, (X * beta).A.ravel(), '-', color = 'IndianRed', label='OLS + AR(1)')

date_ticks = np.linspace(np.min(days_plain), np.max(days_plain), 6).astype('int')
plt.xticks(date_ticks, grace.times.days_to_str(date_ticks))
plt.xlim(np.min(days_plain), np.max(days_plain))

plt.ylabel('EWH [m]')
plt.legend(loc=1)

fig.savefig('../Rapport/figures/ar-compare.pdf')
