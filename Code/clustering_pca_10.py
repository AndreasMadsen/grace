
import grace
import grace.times
import grace.ols
import numpy as np
import matplotlib.pyplot as plt
import cPickle as pickle
import sklearn.mixture as skm
import sklearn.cluster as skc
import time
import mpl_toolkits.basemap as maps
import matplotlib as mpl
import grace
import grace.times

days=grace.ols.time_vector()


def plot_clusters(model,X,w1):
	y=model.predict(X)
	y=y.reshape(180,360)[::-1]
	#print y.shape
	fig = plt.figure(figsize=(12, 6))

	m = maps.Basemap(projection='cyl', lon_0=0, resolution='c')
	m.drawcoastlines(linewidth=2.5, color="white")
	m.drawparallels(np.arange(-90.,120.,30.), labels=[1,0,0,0])
	m.drawmeridians(np.arange(0.,420.,60.), labels=[0,0,0,1])
	
	centroids=model.means_
	cmap=plt.cm.jet
	cmaplist=[cmap(i) for i in range(cmap.N)]
	cmap=cmap.from_list('Custom cmap',cmaplist,cmap.N)
	bounds=np.linspace(0,len(centroids),len(centroids)+1)
	norm=mpl.colors.BoundaryNorm(bounds,cmap.N)
	
	im = m.imshow(y,cmap=cmap,norm=norm)
	plt.title('Clusters')
	
	fig = plt.figure(figsize=(12, 6))
	
	labels=model.predict(centroids)
#	print centroids,model.weights_,labels
	for i,series in enumerate(centroids):
		plt.plot(range(1,11), series.ravel(),lw=2,c=cmap(norm( [float(labels[i])] )).ravel())
	plt.title('Cluster centroids')


	plt.show()

	return 0

def load_network():
	network=pickle.load(open(
				'HPC-output/network.pickle','rb'))
	return network

def display_SA():
	w1,w2,b1,b2=load_network()
	#print w1.shape
	fig=plt.figure(figsize=(12,6))
	plt.plot(w1.T)
	plt.title('w1')
	plt.show()
	return 

#sigmoid activation funtion
def activation(x):
	return 1.0/(1.0+np.exp(-x))

def fit_gmm(X):
	print 'fitting full gaussian mixture model'
	start=time.time()
	model=skm.GMM(n_components=8,covariance_type='full'
			,random_state=1337,n_iter=100,thresh=0.01,n_init=1)
	model.fit(X)
	end=time.time()
	print 'Fit done in ' + str(end-start) + ' seconds.'
	return model
def pca_fit(X):
	print 'calculating singular value decomposition'
	U,S,V = np.linalg.svd(Y.T, full_matrices=False)
	U,S,V = (U, np.diag(S), V.T)
	S_diag = np.diag(S)
	rho = (S_diag**2) / (S_diag**2).sum()
	print 'variance explained: ',rho[:10].sum()
	return np.dot(X,V[:,:10])

if __name__=='__main__':
	print 'Clustering in the autoencoded space.'
#	display_SA()
#	loading (Y is transposed such that days are on rows and positions on columns)
	shape=grace.load.grids.shape
	Y=grace.load.grids.reshape(shape[0]*shape[1],shape[2]).T
	#loading weight matrices and b vectors
	w1,w2,b1,b2=load_network()
	#print Y.shape,w1.shape,np.dot(w1,Y).shape
	#Y_encoded is now 10 by 64800
	#Y_encoded=activation(np.dot(w1,Y)+b1)
	#transposing to comply with scikit
	#Y_encoded=Y_encoded.T
	Y_encoded=pca_fit(Y.T)
	model=fit_gmm(Y_encoded)
	plot_clusters(model,Y_encoded,w1)
