
import sklearn.base
import numpy as np
import math
import time

class GAP:
	def __init__(self, verbose=False):
		self.ks = np.asarray(range(1, 5))
		self.sims = 5
		self._verbose = verbose;
		self._allocate()
		if (self._verbose): print "GAP initialized"

	def dump(self):
		return {
			'ks': self.ks,
			'sims': self.sims,
			'real_W': self._real_W,
			'sim_W': self._sim_Ws
		}
		if (self._verbose): print "Dumped internal GAP result"

	def load(self, dump):
		self.ks = dump['ks']
		self.sims = dump['sims']
		self._real_W = dump['real_W']
		self._sim_Ws = dump['sim_W']
		if (self._verbose): print "Loaded internal GAP result"

	def _allocate(self):
		self._real_W = np.zeros((len(self.ks),          ))
		self._sim_Ws = np.zeros((len(self.ks), self.sims))

	def calculate(self, X, model, ks=None, sims=None):
		"""
			X: data matrix that the uniform distribution will be created from.
			model: scikit-learn estimator, only Kmeans have been tested.
			ks: list of ks to try.
			sims: number of simulations.
		"""

		# Update default parameters if set
		if (ks is not None): self.ks = np.asarray(ks);
		if (sims is not None): self.sims = sims;
		if (ks is not None or sims is not None): self._allocate()

		# Generate simulated data
		tick = time.clock()
		self._sim_data(X)
		self._data = X
		tock = time.clock()
		if (self._verbose): print "Generated simulation data (%.3f s)" % (tock - tick)

		# For each amount of cluster do the calculations
		for i, K in enumerate(self.ks):
			# Use the given model but overwrite the amount of clusters
			estimator = sklearn.base.clone(model, safe=True)
			estimator.set_params(**{ "n_clusters": K })
			self._cluster(i, estimator)

	def _sim_data(self, X):
		shape = X.shape
		tops = X.max(axis=0)
		bots = X.min(axis=0)
		dists = np.matrix(np.diag(tops-bots))
		rands = np.random.random_sample(size=(shape[0], shape[1], self.sims))
		for i in range(0, self.sims):
			rands[:,:,i] = (rands[:,:,i] * dists) + bots

		self._rands = rands

	def _cluster(self, Ki, model):
		if (self._verbose): print "Calculating scores using %d clusters" % (self.ks[Ki])
		# Fit model on actual data
		tick = time.clock()
		self._real_W[Ki] = self._score(model, self._data)
		tock = time.clock()
		if (self._verbose): print "    real data score (%.3f s)" % (tock - tick)

		# Fit model on simulated data
		for Si in range(0, self.sims):
			tick = time.clock()
			self._sim_Ws[Ki, Si] = self._score(model, self._rands[:, :, Si])
			tock = time.clock()
			if (self._verbose): print "    simulated data (%d/%d) score (%.3f s)" % (Si+1, self.sims, tock - tick)

	def _score(self, model, data):
		estimator = sklearn.base.clone(model, safe=True)
		distances = estimator.fit_transform(data)
		groups = estimator.predict(data)
		clusters = distances.shape[1]

		score = 0
		for k in range(0, clusters):
			score += np.power(distances[groups == k, k], 2).sum()

		return score

	def optimal(self):
		real_W = np.log(self._real_W)
		sim_W = np.log(self._sim_Ws)
		sim_W_mean = np.mean(sim_W, axis=1)

		G = sim_W_mean - real_W
		sd = np.std(sim_W, axis=1) * math.sqrt(1 + (1/self.sims))

		opti_k = self.ks[-1]
		for i in range(0, self.ks.shape[0] - 1):
			if (G[i] >= G[i + 1] - sd[i + 1]):
				opti_k = self.ks[i]
				break

		return (opti_k, G, sd)
