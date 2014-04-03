
import grace
import grace.ols
import numpy as np
import matplotlib.pyplot as plt

X = grace.ols.design_matrix()
description = grace.ols.theta_description()

# SVD factorize the X matrix, allowing for numerical stable calculation of
# the hat matrix (H)
U,S,V = np.linalg.svd(X, full_matrices=False)
U,S,V = (U, np.diag(S), V.T)

# Compute cov matrix without sigma^2 (makes it meaning full for all positions)
S2inv = np.diag(np.diag(S)**(-2))
cov = np.asarray(V * S2inv * V.T)

plt.imshow(cov, interpolation='nearest')

plt.colorbar()

plt.xticks(np.arange(0, len(description)), description, fontsize = 10)
plt.setp(plt.xticks()[1], rotation=-90)

plt.yticks(np.arange(0, len(description)), description, fontsize = 10)

plt.title('V * S^-2 * V^T')

plt.tight_layout()
plt.show()
