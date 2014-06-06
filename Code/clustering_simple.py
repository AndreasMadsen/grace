
import grace
import grace.times
import grace.ols
import numpy as np
import matplotlib.pyplot as plt
import sklearn.cluster as skc
import sklearn.metrics as skm
import time
import mpl_toolkits.basemap as maps
import matplotlib as mpl

# get x values (in days)
days = grace.ols.time_vector()


# Get the ewh values with days on columns and position on rows
shape = grace.load.grids.shape
Y = np.asmatrix(grace.load.grids.reshape(shape[0] * shape[1], shape[2]))

def fit_cluster(X):
	batch_size=10000
	print 'Fitting clustering models'
	start=time.time()
	"""
	for i in range(5):
		i=i+2
		model=skc.MiniBatchKMeans(init='k-means++',
			n_clusters=i,batch_size=batch_size).fit(X)
		print i,skm.silhouette_score(X,
			model.labels_,metric='euclidean',sample_size=1000)
	"""
	end=time.time()
	
	model=skc.MiniBatchKMeans(init='k-means++',
			n_clusters=10,batch_size=batch_size*2).fit(X)
	print 'Models done in ' + str(end-start)  + ' seconds.'
	return model

def plot_clusters(model):
	x=model.labels_
	x=x.reshape(180,360)[::-1]
	print x.shape
	fig = plt.figure(figsize=(12, 6))

	m = maps.Basemap(projection='cyl', lon_0=0, resolution='c')
	m.drawcoastlines(linewidth=2.5, color="white")
	m.drawparallels(np.arange(-90.,120.,30.), labels=[1,0,0,0])
	m.drawmeridians(np.arange(0.,420.,60.), labels=[0,0,0,1])
	
	centroids=model.cluster_centers_
	cmap=plt.cm.jet
	cmaplist=[cmap(i) for i in range(cmap.N)]
	cmap=cmap.from_list('Custom cmap',cmaplist,cmap.N)
	bounds=np.linspace(0,len(centroids),len(centroids)+1)
	norm=mpl.colors.BoundaryNorm(bounds,cmap.N)
	
	im = m.imshow(x,cmap=cmap,norm=norm)
	plt.title('Clusters')
	
	fig = plt.figure(figsize=(12, 6))

	labels=model.predict(centroids)
	for i,series in enumerate(centroids):
		plt.plot(days, series.ravel(),lw=2,c=cmap(norm( [float(labels[i])] )).ravel())
	plt.title('Centroids')
	plt.show()

	return 0

if __name__=='__main__':
	print Y.shape
	model=fit_cluster(Y[:,:])
	plot_clusters(model)

