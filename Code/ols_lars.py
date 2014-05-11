
import grace
import grace.times
import grace.ols
import numpy as np
import matplotlib.pyplot as plt
import sklearn.linear_model as lm
initial = (24, 134)

# get x values (in days)
days = grace.ols.time_vector()
all_days = np.linspace(np.min(days), np.max(days), np.max(days) - np.min(days))

# Get the ewh values for this position
Y = np.asarray(grace.grids[initial[0], initial[1], :])
#get theta
Theta = grace.ols.theta_vector(Y)
#get description
description = grace.ols.theta_description()
#get X
X=grace.ols.design_matrix(days)

#!!!#
#LARS
#!!!#
myAlpha=0.005
alphas, _, coefs = lm.lars_path(X.A, Y, method='lasso', verbose=True)
#uncomment the following if you want verbose:
#print 'model coefficients: ',model.coef_

fig = plt.figure()
beta=np.asmatrix(coefs[:,7]).T
print beta.shape, X.shape
print (X*beta).shape, days.shape
# Plot
plt.plot
plt.plot(days, Y.ravel(), 'ro',label='Observations')
plt.plot(all_days, (grace.ols.design_matrix(all_days) * Theta).A.ravel(),'k-',lw=1,label='Linear Regression')
plt.plot(days.ravel(),(X*beta).A.ravel(),'b-',lw=1,label='LARS,7 non zero elements')
plt.legend(loc=3)

date_ticks = np.linspace(np.min(days), np.max(days), 6).astype('int')
plt.xticks(date_ticks, grace.times.days_to_str(date_ticks))
plt.xlim(np.min(days), np.max(days))

plt.ylabel('EWH [m]')
plt.xlabel('date')

#coefficients
print '\n'
print coefs[:,7][:7]
print description[:7]


scaledY=(coefs.T/np.abs(coefs[:,-1]))
print coefs.T.shape,scaledY.shape,alphas.shape
plt.figure()
plt.plot(range(40),coefs.T)

plt.xlabel('Iteration')
plt.ylabel('Coefficients')
plt.title('LASSO Path')
plt.xticks()

#the following is commented because 1 coefficient has such big fluctuations that the plot is unreadable
"""
plt.figure()
print np.tile(alphas,[39,1]).shape, scaledY.shape
plt.plot(np.tile(alphas,[39,1]).T,scaledY)

plt.xlabel('alpha')
plt.ylabel('Coefficient/|Final coefficient value|')
plt.title('LASSO Path')
plt.xticks()
"""

plt.figure()
plt.plot(range(40),scaledY)

plt.xlabel('Iteration')
plt.ylabel('Coefficient/|Final coefficient value|')
plt.title('LASSO Path')
plt.show()


