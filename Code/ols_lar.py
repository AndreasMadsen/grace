
import grace
import grace.times
import grace.ols
import numpy as np
import matplotlib.pyplot as plt
import sklearn.linear_model as lm

initial = (26, 130)

# get x values (in days)
days = grace.ols.time_vector()
all_days = np.linspace(np.min(days), np.max(days), np.max(days) - np.min(days))

# Get OLS stuff for this position
Y = grace.grids[initial[0], initial[1], :]
Theta = grace.ols.theta_vector(Y)
description = grace.ols.theta_description()
X = grace.ols.design_matrix(days)
X_all = grace.ols.design_matrix(all_days)
#
# Least Angular Regression
#
_, _, coefs = lm.lars_path(X.A, Y, method='lar')
beta = np.asmatrix(coefs[:,7]).T
#
# Generate compare figure
#
fig = plt.figure(figsize=(10, 6))

# Plot y and y.hat
plt.scatter(days, Y.ravel(), color="SteelBlue", alpha=0.7)
plt.plot(all_days, (X_all * Theta).A.ravel(), color="black", label='OLS')
plt.plot(all_days.ravel(), (X_all*beta).A.ravel(), color="IndianRed", label='LAR, 7 parameters')

date_ticks = np.linspace(np.min(days), np.max(days), 6).astype('int')
plt.xticks(date_ticks, grace.times.days_to_str(date_ticks))
plt.xlim(np.min(days), np.max(days))
plt.ylabel('EWH [m]')

plt.legend(loc=1)
fig.savefig('../Rapport/figures/lar-compare.pdf')

#
# Print coefficients
#
for i, name in enumerate(description):
	if (coefs[i,7] != 0.0):
		print "%s: %e" % (name, coefs[i,7])

scaledY = (coefs.T/np.abs(coefs[:,-1]))

#
# Plot lasso path
#
fig = plt.figure(figsize=(10, 4))
plt.plot(range(0, len(description) + 1), scaledY)

plt.xlabel('Iteration')
plt.ylabel('relative coefficients')
plt.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.15)
fig.savefig('../Rapport/figures/lar-coefficients.pdf')

plt.show()
