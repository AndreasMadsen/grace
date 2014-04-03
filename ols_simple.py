
import grace
import grace.times
import grace.ols
import numpy as np
import matplotlib.pyplot as plt

initial = (24, 134)

# get x values (in days)
days = grace.ols.time_vector()
all_days = np.linspace(np.min(days), np.max(days), np.max(days) - np.min(days))

# Get the ewh values for this position
Y = np.asmatrix(grace.grids[initial[0], initial[1], :]).T
Theta = grace.ols.theta_vector(Y)
description = grace.ols.theta_description()

fig = plt.figure()

# Plot y and y.hat
plt.subplot(2,1,1)
plt.plot(days, Y.A.ravel(), 'ro',label='Observations')
plt.plot(all_days, (grace.ols.design_matrix(all_days) * Theta).A.ravel(),'k-',label='Estimation')

date_ticks = np.linspace(np.min(days), np.max(days), 6).astype('int')
plt.xticks(date_ticks, grace.times.days_to_str(date_ticks))
plt.xlim(np.min(days), np.max(days))

plt.ylabel('EWH [m]')
plt.xlabel('date')

# Plot theta values
plt.subplot(2,1,2)
plt.bar((np.arange(0, Theta.size) + 0.5).ravel(), Theta.A.ravel())
plt.xlim(0, Theta.size + 1)
plt.xticks(np.arange(1, Theta.size + 1), description)
plt.setp(plt.xticks()[1], rotation=-80)

plt.show()