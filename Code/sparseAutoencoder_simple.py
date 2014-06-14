import sAe
import numpy as np
import grace
import time
import cPickle as pickle

visible_size = 341
hidden_size = 196


options = sAe.SparseAutoEncoderOptions(visible_size,hidden_size,
  output_dir="HPC-output", max_iterations = 400)




if __name__=='__main__':
  print 'Running sparse autoencoder'
  print 'Loading data'
  start=time.time()
  shape=grace.load.grids.shape
  Y=grace.load.grids.reshape(shape[0]*shape[1],shape[2])
  end=time.time()
  print 'Loading done in ' + str(end-start) + ' seconds.'

  network=sAe.SparseAutoEncoder(options=options, data=Y.T)# Y[:1000].T
  
  print 'Training sparse autoencoder'
  start=time.time()
  solutions = network.learn()
  end=time.time()
  print 'Fit done in ' + str(end-start) + ' seconds.'

  print 'Writing output to files'
  output = open("./HPC-output/network.pickle", "wb")
  output.write(pickle.dumps(solutions))
  output.close()
  print 'Done'
