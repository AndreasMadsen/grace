
import math
import numpy as np
import grace
import grace.ols
import matplotlib.pyplot as plt
import mpl_toolkits.basemap as maps
import matplotlib.gridspec as gridspec

H = grace.ols.hat_matrix()

# Get the ewh values for all positions as a matrix. This matrix
# will have the diffrent positons as collums and days on the rows
shape = grace.grids.shape
Y = np.asmatrix(grace.grids.reshape(shape[0] * shape[1], shape[2])).T

# Calculate residuals (collums: position, rows: days)
e = Y - H * Y

# Do SVD of residuals (transposed)
U,S,V = np.linalg.svd(e.T, full_matrices=False)
U,S,V = (U, np.diag(S), V.T)

# Transform U intro a (lat, lon, day) ndarray
U_grid = np.asarray(U.T).reshape(shape[2], shape[0], shape[1]).transpose([1,2,0])

#
# Plot Theta parameter for all positions
#
dayIndex = 3

fig = plt.figure(figsize=(12, 9))

gs = gridspec.GridSpec(3, 3)

plt.subplot(gs[:-1, :])
m = maps.Basemap(projection='cyl', lon_0=0, resolution='c')
m.drawcoastlines(linewidth=.5)
m.drawparallels(np.arange(-90.,120.,30.), labels=[1,0,0,0])
m.drawmeridians(np.arange(0.,420.,60.), labels=[0,0,0,1])

im = m.imshow(U_grid[::-1,:,dayIndex])
im.set_cmap('binary_r')

m.colorbar()

plt.title("index: " + str(dayIndex))

plt.subplot(gs[-1, :-1])

S_diag = np.diag(S)
rho = (S_diag**2) / (S_diag**2).sum()

bars = plt.bar(range(0, rho.shape[0]), rho * 100, color='SteelBlue')
bars[dayIndex].set_color('IndianRed')

plt.xlim(0, rho.shape[0] / 3)
plt.title('Variance explained by principal components')
plt.xlabel('Principal component')
plt.ylabel('%')

plt.subplot(gs[-1, -1])

plt.plot(range(0, V.shape[0]), V[:, dayIndex].A.ravel(), color="SteelBlue")
plt.xlim(0, V.shape[0])

plt.show()


