# -*- coding: utf-8 -*-

import grace
import grace.times
import grace.ols
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.basemap as maps

# Compute the hat matrix
fig = plt.figure(figsize=(8, 5))
days = grace.ols.time_vector()
H = np.diag(grace.ols.hat_matrix())

# Plot y and y.hat
plt.plot(days, H.ravel(), '-x', color="SteelBlue", label='H diagonal')

# Set ticks
date_ticks = np.linspace(np.min(days), np.max(days), 6).astype('int')
plt.xticks(date_ticks, grace.times.days_to_str(date_ticks))
plt.xlim(np.min(days), np.max(days))

# Set labels
plt.ylabel('H diagonal')

if (__name__ == '__main__'): plt.show()
