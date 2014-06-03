
import grace
import grace.times
import grace.ols
import numpy as np
import matplotlib.pyplot as plt
import sklearn.cluster as skc
import sklearn.metrics as skm
import time
import mpl_toolkits.basemap as maps

# Get the ewh values with days on columns and position on rows
shape = grace.load.grids.shape
Y = np.asmatrix(grace.load.grids.reshape(shape[0] * shape[1], shape[2]))

def fit_cluster(X):
	batch_size=10000
	print 'Fitting clustering models'
	start=time.time()
	for i in range(5):
		i=i+2
		model=skc.MiniBatchKMeans(init='k-means++',
			n_clusters=i,batch_size=batch_size).fit(X)
		print i,skm.silhouette_score(X,
			model.labels_,metric='euclidean',sample_size=1000)
	end=time.time()
	model=skc.MiniBatchKMeans(init='k-means++',
			n_clusters=5,batch_size=batch_size*2).fit(X)
	print 'Models done in ' + str(end-start)  + ' seconds.'
	return model

def plot_clusters(model):
	x=model.labels_
	x=x.reshape(180,360)
	print x.shape
	fig = plt.figure(figsize=(12, 6))

	m = maps.Basemap(projection='cyl', lon_0=0, resolution='c')
	m.drawcoastlines(linewidth=.5, color="white")
	m.drawparallels(np.arange(-90.,120.,30.), labels=[1,0,0,0])
	m.drawmeridians(np.arange(0.,420.,60.), labels=[0,0,0,1])
	
	im = m.imshow(x)
	plt.title('Clusters')
	plt.show()
if __name__=='__main__':
	print Y.shape
	model=fit_cluster(Y[:,:])
	plot_clusters(model)

