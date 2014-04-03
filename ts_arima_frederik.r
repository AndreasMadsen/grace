#Setup
cat("\014")
rm(list = ls())
setwd(dirname(sys.frame(1)$ofile))
#setwd("C:/Users/Frederik/Google Drev/01666 - fagprojekt/Code")
par(pty="m", mfrow=c(1,1))

#instal
library(astsa) #nicer time series interface
library(forecast) #nicer forecasting interface

# Load data
interpolated = read.table('ts_greenland.csv',sep=',')

#
# Time Series Analysis Stuff
#

train=ts(head(interpolated,length(interpolated)-12))
plot(train)
test=ts(tail(interpolated,12), start=c(end(train)[1] + 1))
#freq around 36ish=?
differenceTrain=diff(train,1)
plot(differenceTrain)

par(mar=c(3,3,3,1),mgp=c(2,0.7,0))
acf(differenceTrain,36*5)
#non-seasonal ma: 4 (6?)
#seasonal 4-5ish
pacf(differenceTrain,36*5)
#non-seasonal ar: 3
#seasonal 1ish

#inital model
#warning: the sma will make this fit take a long time!
start<-sarima(train,3,1,3,1,1,4,36,no.constant=TRUE);start
#loads of non-significant parameters (statistically)

#iteratively fit and check temp model. remove least signifanct
#until final model is reach
tmp<-sarima(train,3,1,2,0,1,1,36,no.constant=TRUE);tmp

final<-sarima(train,3,1,2,0,1,1,36,no.constant=TRUE);final
#as i evident from the ljung-box statistics something is wrong:
plot(train,type='p')
lines(train+final$fit$residuals,col='red',type='l')
#alot of "spikes" where there is none in data. 
#speculation: This could be because of how the GRACE data is constructed
#as a combination of values observed/and/or because of estimation of missing data
#being made with a method that regresses towards the mean where it shouldn't.

#it seems that it's the upturns (Greenland's winter) that the model has the hardest
#time predicting.

#nicer forecasting interface to R's predict.Arima
myPred<-sarima.for(train,length(test),3,1,2,0,1,1,36,no.constant=TRUE)
lines(test,col='green')

#standard auto fitter:
#this fails  -  could be a sign that 
#arima without exogen factors can't model the data
stl(interpolated$V1)
