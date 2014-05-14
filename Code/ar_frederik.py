
import grace
import grace.times
import grace.ols
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import scipy.interpolate as si

initial = (24, 134)

# get x values (in days)
days = grace.ols.time_vector()
all_days = np.linspace(np.min(days), np.max(days), np.max(days) - np.min(days))

# Get the ewh values for this position
Y = np.asmatrix(grace.grids[initial[0], initial[1], :]).T
Theta = grace.ols.theta_vector(Y)
description = grace.ols.theta_description()

#interpolating to get equidistant ts

interpolater=si.interp1d(days,Y.ravel(),kind='linear')
equi=np.linspace(days[0],days[-1],1+(days[-1]-days[0])/(days[1]-days[0]))
interpolated_Y=np.matrix(interpolater(equi)).T
print interpolated_Y.shape

#using statsmodels for quick durbin watson test of autocorrelated residuals
X=grace.ols.design_matrix(equi)
model=sm.OLS(interpolated_Y,X)
initial_results=model.fit()
print initial_results.summary()
#durbin-watson is less, than 1.0 (it's 0.228)!! - this suggests correlation




#Fitting regression model with statsmodels package
model=sm.GLSAR(interpolated_Y,X,rho=1)
for i in range(100):
	result=model.fit()
	#uncomment the following line to check convergence:
	#print "coefficients for AR-process on residuals: "+str(model.rho)
	rho,sigma=sm.regression.yule_walker(result.resid, order=model.order)
	model=sm.GLSAR(interpolated_Y,X,rho)

print result.summary()
print "coefficients for AR-process on residuals: "+str(model.rho)


print "coefficient diff: "+str((result.params-Theta.ravel()))
fig = plt.figure()

# Plot y and y.hat
plt.subplot(1,1,1)
plt.plot(equi, interpolated_Y.A.ravel(), 'ro',alpha=0.5,label='Observations')

plt.plot(equi, initial_results.fittedvalues,'k-',lw=1.5,label='OLS')
plt.plot(equi, result.fittedvalues,'g-',lw=1.5,label='AR-OLS')
plt.legend(loc=1)
date_ticks = np.linspace(np.min(equi), np.max(equi), 6).astype('int')
plt.xticks(date_ticks, grace.times.days_to_str(date_ticks))
plt.xlim(np.min(equi), np.max(equi))

plt.ylabel('EWH [m]')
plt.xlabel('date')

# Plot theta values
#plt.subplot(2,1,2)
#plt.bar((np.arange(0, Theta.size) + 0.5).ravel(), Theta.A.ravel())
#plt.xlim(0, Theta.size + 1)
#plt.xticks(np.arange(1, Theta.size + 1), description)
#plt.setp(plt.xticks()[1], rotation=-80)

plt.show()
