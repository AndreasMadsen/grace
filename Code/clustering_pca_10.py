
import grace
import grace.times
import grace.ols
import numpy as np
import matplotlib.pyplot as plt
import cPickle as pickle
import sklearn.mixture as skm
import sklearn.decomposition as skd
import time
import mpl_toolkits.basemap as maps
import matplotlib as mpl
import grace
import grace.times

days=grace.ols.time_vector()
number_of_pcs=10

colors_hex = [
	"a6cee3", "1f78b4", "b2df8a", "33a02c", "fb9a99", "e31a1c",
	"fdbf6f", "ff7f00", "cab2d6", "6a3d9a", "ffff99", "b15928","edf8b1"
	,"bcbddc", "636363", 
]
colors_rgb = map(lambda hex: [ord(c) for c in hex.decode('hex')], colors_hex)


def write_latex_table(x,v):
	print 'writing latex table'
	covs=np.zeros([341,x.shape[0]])
	print covs.shape
	for i,elem in enumerate(x):
		covs[:,i]=1.96*np.sqrt(np.dot(np.diag(elem).reshape(1,number_of_pcs), v.T[:number_of_pcs]))
	with open('HPC-output/covariance_structure.txt','wb') as f:
		f.write('\\begin{tabular}{l|c|c|c|c|c|c|c|c}')
		f.write('\n\tday')
		for i in range(8):
			f.write(' &\t cluster ' +str(i))
		f.write(' \\\\')
		for i,row in enumerate(covs):
			f.write('\n\t'+str(i+1))
			for elem in row:
				f.write('\t & ' + str(elem))
			f.write('\\\\')

		f.write('\n\\end{tabular}')
			
	print 'latex table written'
	

def plot_pca_clusters(model,kpca,X):
	y=model.predict(X)
	y=y.reshape(180,360)[::-1]
	shape=y.shape
	#print y.shape
	fig = plt.figure(figsize=(12, 6))

	m = maps.Basemap(projection='cyl', lon_0=0, resolution='c')
	m.drawcoastlines(linewidth=2.5, color="white")
	m.drawparallels(np.arange(-90.,120.,30.), labels=[1,0,0,0])
	m.drawmeridians(np.arange(0.,420.,60.), labels=[0,0,0,1])
	
	centroids=model.means_
	covariance=model.covars_

	cmap=plt.cm.jet
	cmaplist=[cmap(i) for i in range(cmap.N)]
	cmap=cmap.from_list('Custom cmap',cmaplist,cmap.N)
	bounds=np.linspace(0,len(centroids),len(centroids)+1)
	norm=mpl.colors.BoundaryNorm(bounds,cmap.N)
	
	world = np.ones((shape[0], shape[1], 3)).astype('uint8') * 255

	for i in range(0,shape[0]):
		for j in range(0,shape[1]):
			world[i,j,:]=colors_rgb[y[i,j]]
	
	im = m.imshow(world,cmap=cmap,norm=norm)
	plt.title('KPCA Clustering')
	fig.savefig('HPC-output/kpca-world.png')
	fig = plt.figure(figsize=(12, 6))
	labels=model.predict(centroids)
#	print centroids,model.weights_,labels
	for i,series in enumerate(kpca.inverse_transform(centroids)):
		plt.plot(days, series.ravel(),lw=2,c='#' + colors_hex[i],label='cluster '+str(i+1))
	
	plt.legend(loc=3)
	plt.title('Cluster centroids (inverse transformed kpca)')

	fig.savefig('HPC-output/kpca-centroids.png')
	return 0


def fit_gmm(X):
	print 'fitting full gaussian mixture model'
	start=time.time()
	model=skm.GMM(n_components=12,covariance_type='full'
			,random_state=1337,n_iter=100,thresh=0.01,n_init=1)
	model.fit(X)
	end=time.time()
	print 'Fit done in ' + str(end-start) + ' seconds.'
	return model

def pca_fit(X):
	print 'calculating singular value decomposition'
	U,S,V = np.linalg.svd(Y, full_matrices=False)
	U,S,V = (U, np.diag(S), V.T)
	S_diag = np.diag(S)
	rho = (S_diag**2) / (S_diag**2).sum()
	print 'variance explained: ',rho[:number_of_pcs].sum()
	return [np.dot(X,V[:,:number_of_pcs]),V]

def kernel_pca_fit(X):
	model=skd.KernelPCA(n_components=number_of_pcs,degree=3,kernel='rbf',gamma=None,fit_inverse_transform=True)
	X_kpca=model.fit_transform(X)
	return [X_kpca,model]

if __name__=='__main__':
	print 'Clustering in the (kernel)PCA space.'
#	display_SA()
#	loading ( position are on rows and days on columns)
	shape=grace.load.grids.shape
	Y=grace.load.grids.reshape(shape[0]*shape[1],shape[2])

	#[Y_encoded,v]=pca_fit(Y)
	[Y_encoded,kpca]=kernel_pca_fit(Y)
	model=fit_gmm(Y_encoded)
	#plot_clusters(model,Y_encoded,v)
	plot_pca_clusters(model,kpca,Y_encoded)
