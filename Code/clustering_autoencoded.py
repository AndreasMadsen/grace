
import grace
import grace.times
import grace.ols
import numpy as np
import matplotlib.pyplot as plt
import cPickle as pickle

def display_SA():
	network=pickle.load(open(
				'HPC-output/network.pickle','rb'))
	w1,w2,b1,b2=network
	print w1.shape
	fig=plt.figure(figsize=(12,6))

	plt.plot(w1.T)
	plt.show()
	print 'test'
	return 
if __name__=='__main__':
	display_SA()
