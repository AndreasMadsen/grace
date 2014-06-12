import cPickle as pickle
import matplotlib.pyplot as plt
import numpy as np
def load():
	res=pickle.load(open('HPC-output/gap.res','rb'))
	print 'gap: ', res[0]
	print 'sd: ',res[1]
	return res

if __name__=="__main__":
	print 'plotting gap statistics'
	[g,s]=load()
	x=np.asarray(range(len(g)))+1
	plt.figure(figsize=(12,6))
	plt.plot(x,g,label='GAP')
	plt.plot(x,g+s,label='GAP+SD')
	plt.plot(x,g-s,label='GAP-SD')
	plt.legend(loc=4)
	plt.xticks(x)
	plt.savefig('figures/gap.png')
	plt.show()
	exit(0)
