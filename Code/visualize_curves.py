
import grace
import grace.times
import grace.ols
import numpy as np
import matplotlib.pyplot as plt

initial = (24, 134)

# get x values (in days)
days = grace.ols.time_vector()
all_days = np.linspace(np.min(days), np.max(days), np.max(days) - np.min(days))

# Get the ewh values on columns, and positions on rows
shape = grace.load.grids.shape
Y = np.asmatrix(grace.load.grids.reshape(shape[0] * shape[1], shape[2]))
Y=Y.A

fig = plt.figure(figsize=(12,6))

# Plot y 
r=Y.shape[0]-50000
for i in range(r):
	print 'Processing location ' + str(i+1) + ' out of  ' + str(r)
	plt.plot(days, Y[i,:], 'b-',label='Observations',alpha=0.05)


date_ticks = np.linspace(np.min(days), np.max(days), 6).astype('int')
plt.xticks(date_ticks, grace.times.days_to_str(date_ticks))
plt.xlim(np.min(days), np.max(days))

plt.ylabel('EWH [m]')
plt.xlabel('date')

print 'saving and plotting figure'
fig.savefig("../Rapport/figures/transparent_lines.png")
plt.show()
