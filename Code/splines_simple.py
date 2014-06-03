
import grace
import grace.times
import grace.ols
import numpy as np
import matplotlib.pyplot as plt

# (41, 77) and (89, 186) is not completly continues
initial = (24, 134)

# get x values (in days)
days = grace.ols.time_vector()
all_days = np.linspace(np.min(days), np.max(days), np.max(days) - np.min(days))

# Get the ewh values for this position
Y = np.asmatrix(grace.grids[initial[0], initial[1], :]).T
X_all = grace.ols.design_matrix(all_days, frequencies = 3, splines = True)
Theta = grace.ols.theta_vector(Y, frequencies = 3, splines = True)
description = grace.ols.theta_description(frequencies = 3, splines = True)

## Plot y and y.hat
plt.figure()
plt.subplot(2,1,1)
plt.plot(days, Y.A.ravel(), 'ro',label='Observations')
plt.plot(all_days, (X_all * Theta).A.ravel(),'k-',label='Estimation')

date_ticks = np.linspace(np.min(days), np.max(days), 6).astype('int')
plt.xticks(date_ticks, grace.times.days_to_str(date_ticks))
plt.xlim(np.min(days), np.max(days))
plt.ylim(np.min(Y), np.max(Y))

plt.ylabel('EWH [m]')
plt.xlabel('date')

# Plot theta values
plt.subplot(4,1,3)
plt.bar((np.arange(0, Theta.size) + 0.5).ravel(), Theta.A.ravel())
plt.xlim(0, Theta.size + 1)
plt.xticks(np.arange(1, Theta.size + 1), description)
plt.setp(plt.xticks()[1], rotation=-90, fontsize = 10)

# How may splines (the years parameter calculated internally in module.ols)
splines = 9

plt.figure(figsize=(12,6))

# Intercept
plt.subplot(4,1,1)
plt.plot(all_days, X_all[:,0].A.ravel())

# Slope
plt.subplot(4,1,2)
plt.plot(all_days, X_all[:,1].A.ravel())

# Acceleration
plt.subplot(4,1,3)
plt.plot(all_days, X_all[:,2].A.ravel())

# Full Year
plt.subplot(4,1,4)
for i in range(0,splines + 1):
	plt.plot(all_days, X_all[:,i * 2 + 3].A.ravel())
	plt.plot(all_days, X_all[:,i * 2 + 4].A.ravel())
plt.savefig('../Rapport/figures/splines.png')
plt.show()
