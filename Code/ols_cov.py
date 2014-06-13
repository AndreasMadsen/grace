
import grace
import grace.ols
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

X = grace.ols.design_matrix()
description = grace.ols.theta_description()
description = ['$' + text.replace('(t)', 't') + '$' for text in description]
description[1] = '$vel. (t)$'

# SVD factorize the X matrix, allowing for numerical stable calculation of
# the hat matrix (H)
U,S,V = np.linalg.svd(X, full_matrices=False)
U,S,V = (U, np.diag(S), V.T)

# Compute cov matrix without sigma^2 (makes it meaning full for all positions)
S2inv = np.diag(np.diag(S)**(-2))
cov = V * S2inv * V.T
var = np.asmatrix(np.sqrt(np.diag(cov))).T
corr = np.asarray(cov) / np.asarray(var * var.T)

fig = plt.figure(figsize=(7,7))

im = plt.imshow(corr, interpolation='nearest', vmax=1, vmin=-1)
im.set_cmap('binary_r')

plt.xticks(np.arange(0, len(description)), description, fontsize = 10)
plt.setp(plt.xticks()[1], rotation=-90)

plt.yticks(np.arange(0, len(description)), description, fontsize = 10)

divider = make_axes_locatable(plt.gca())
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(im, cax=cax)

plt.tight_layout()

if (__name__ == '__main__'): plt.show()
