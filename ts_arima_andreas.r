#Setup
cat("\014")
rm(list = ls())
setwd(dirname(sys.frame(1)$ofile))
par(pty="m", mfrow=c(1,1))

#
# Functions
#
acfplot = function (m, skip=0) {
  dat = ts(m$residuals[(1 + skip):length(m$residuals)], frequency = frequency(m$residuals))
  
  acf(dat, main="ACF of residuals", lag.max=75)
  pacf(dat, main="PACF of residuals", lag.max=75)
}

acfdiag = function (m, skip=0) {
  op <- par(pty="m", mfrow=c(2,1), mai=c(1.1,1.1,1.0,0.2))
  acfplot(m, skip=skip)
  par(op)
}

ljungboxplot = function (m, gof.lag = 10, skip = 0) {
  dat = ts(m$residuals[(1 + skip):length(m$residuals)], frequency = frequency(m$residuals))
  
  pval <- numeric(gof.lag)
  for (i in (length(m$coef)+1):gof.lag) {
    pval[i] <- Box.test(dat, i, type = "Ljung-Box", fitdf=length(m$coef))$p.value
  }
  
  plot(ts(pval[(1 + length(m$coef)):length(pval)], frequency=frequency(m$residuals), start=(length(m$coef))/frequency(m$residuals)),
       xlab = "Lag", ylab = "p value", xaxt="n", type="p",
       ylim = c(0, 1), main = "p values for Ljung-Box statistic"
  )
  axis(1, at=seq(0,3,0.5) - 1/frequency(m$residuals), labels=seq(0,12*3,6))
  abline(h = 0.05, lty = 2, col = "blue")
}

findiag = function (m, gof.lag = 10, skip = 0) {
  dat = ts(
    m$residuals[(1 + skip):length(m$residuals)],
    frequency = frequency(m$residuals),
    start=c(start(m$residuals)[1], start(m$residuals)[2] + skip)
  )
  
  op <- par(pty="m", mfrow=c(2,1), mai=c(1.1,1.1,0.6,0.2))
  ts.plot(dat, ylab="Residuals", col="SteelBlue", main="Residuals")
  abline(c(0,0), col="Gray")
  ljungboxplot(m, gof.lag = gof.lag, skip = skip)
  par(op)
}

signtest = function (m, skip=0) {
  dat = m$residuals[(1 + skip):length(m$residuals)]
  
  sc = 0
  last.sign.negative = (dat[1] < 0)
  for (i in 2:length(dat)) {
    if ((dat[i] < 0) != last.sign.negative) {
      sc = sc + 1
      last.sign.negative = (dat[i] < 0)
    }
  }
  
  print(binom.test(sc, length(dat) - 1, p=0.5))
}
# Load data
y = read.table('ts_greenland.csv',sep=',')
ts.plot(y)

method = "CSS"

#
# Stationarity
#
m = arima(y, order=c(0,1,0), method=method, include.mean=FALSE)
ts.plot(m$residuals)

m = arima(y, order=c(0,1,0), seasonal = list( order=c(0,1,0), period=36.5 ), method=method, include.mean=FALSE)
ts.plot(m$residuals)

#
# Model order
#
acfdiag(m, skip=37)
cat("Step 1\n")

m = arima(y, order=c(2,1,0), seasonal = list( order=c(0,1,0), period=36.5 ), method=method, include.mean=FALSE)
acfdiag(m, skip=37)
cat("Step 2\n")

m = arima(y, order=c(2,1,0), seasonal = list( order=c(2,1,0), period=36.5 ), method=method, include.mean=FALSE)
acfdiag(m, skip=37)
cat("Step 3\n")

findiag(m, gof.lag=40, skip=50)

signtest(m)

qqnorm(m$residuals)
qqline(m$residuals)