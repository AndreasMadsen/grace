
import grace
from gap import gap
import numpy as np
import cPickle as pickle



# Get the ewh values with days on columns and position on rows
shape = grace.load.grids.shape
Y = np.asmatrix(grace.load.grids.reshape(shape[0] * shape[1], shape[2]))

if __name__=='__main__':
	#compute gap statistics (see gap.py)
	res=gap(Y.A,nrefs=5,ks=range(1,21))
	pickle.dump(res, open('gap.res','wb'))
	[gaps,SD]=res
	print 'gap-statistics:', gaps
	print 'standard deviation: ', SD
	optimal_clusters=0
	for i,elem in enumerate(gaps):
		if elem != gaps[-1]:
			if elem >= gaps[i+1]-SD[i+1]:
				optimal_clusters=i+1
				print ' according to GAP statistics the optimal cluster amount is:', optimal_clusters 
				exit(0)
		else:
			print 'the optimal number of clusters is greater than the maximal clusters tested.\n\tRerun the script with a greater k'





