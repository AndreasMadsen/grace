#Setup
cat("\014")
rm(list = ls())
setwd(dirname(sys.frame(1)$ofile))
par(pty="m", mfrow=c(1,1))

library(forecast)

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
       xlab = "Lag", ylab = "p value", type="p",
       ylim = c(0, 1), main = "p values for Ljung-Box statistic"
  )
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

qqdiag = function (m, skip=0) {
  dat = ts(
    m$residuals[(1 + skip):length(m$residuals)],
    frequency = frequency(m$residuals),
    start=c(start(m$residuals)[1], start(m$residuals)[2] + skip)
  )
  
  qqnorm(dat)
  qqline(dat)
}

paramdiag = function (m) {
  sided_half = pt(m$coef / sqrt(diag(m$var.coef)), df=(length(m$residuals) - length(m$coef)))
  p_half = apply(rbind(sided_half, 1 - sided_half), 2, min)
  return(  2 * p_half )
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
y = read.table('ts_greenland.csv',sep=',')$V1
y.train = ts(y[1:(length(y)-36)], start=1)
y.test = ts(y[(length(y)-36+1):length(y)], start=length(y.train)+1)

# Plot Cross Validation splits
ts.plot(y.train, col="SteelBlue",
        xlim=c(1, length(y)),
        ylim=c(min(y), max(y)),
        ylab="EWH [m]"
)
lines(y.test, col="#4F8913")

method = "CSS"

#
# Stationarity
#
m = arima(y.train, order=c(0,1,0), method=method, include.mean=FALSE)
ts.plot(m$residuals, col="SteelBlue")

m = arima(y.train, order=c(0,1,0), seasonal = list( order=c(0,1,0), period=36.5 ), method=method, include.mean=FALSE)
ts.plot(m$residuals, col="SteelBlue")

#
# Model order
#
acfdiag(m, skip=37)
cat("Step 1\n")

m = arima(y.train, order=c(2,1,0), seasonal = list( order=c(0,1,0), period=36.5 ), method=method, include.mean=FALSE)
acfdiag(m, skip=39)
cat("Step 2\n")

m = arima(y.train, order=c(2,1,0), seasonal = list( order=c(2,1,0), period=36.5 ), method=method, include.mean=FALSE)
acfdiag(m, skip=111)
cat("Step 3\n")

qqdiag(m, skip=111)
findiag(m, gof.lag=75, skip=111)

signtest(m)

#
# Parameter tests
#

cat("P values:\n")
print(paramdiag(m))

#
# Cross Validation
#
f = forecast(m, h = length(y.test), level=c(95))

ts.plot(y.train, col="SteelBlue",
        xlim=c(1, length(y)),
        ylim=c(min(y), max(y)),
        ylab="EWH [m]"
)
#lines(y.train - m$residuals, col="IndianRed", lwd=0.5)
lines(y.test, col="#4F8913")
lines(f$mean, col="IndianRed", lwd=2)
lines(ts(f$lower, start=start(y.test)), col="LightGray")
lines(ts(f$upper, start=start(y.test)), col="LightGray")
