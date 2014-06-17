
import sklearn.cluster
from kmeans_gap import GAP
import grace
import numpy as np
import matplotlib.pyplot as plt

optimizer = GAP(verbose=True)
optimizer.load(np.load('HPC-output/gap.npz'))

(K, G, sd) = optimizer.optimal()
print "Optimal: %d" % (K)
plt.errorbar(optimizer.ks, G, sd)
plt.show()
