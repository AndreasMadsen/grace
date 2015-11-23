grace
=====

The world coolest analysis of the grace data, made by two crazy kids

## Setup

The code uses python 2.7 and the following modules:

* numpy
* scipy
* matplotlib (with basemap extension)
* scikit-learn
* pandas
* netCDF4

## Scripts

The scripts are categorized by a prefix:

* `ar` and `ts` : auto regression / time series analysis
* `clustering` and `gmm`: GMM clustering analysis
* `ice`: estimation of ice melting (not included in report)
* `kmeans`: K-means clustering analysis
* `ols`: Ordinary Least Squares (OLS) (the primary part)
* `splines`: OLS using splines

There aren't any documentation for the scripts as we where only judged on the
report and the results not the code. If you are interested in the code, the
best strategy is to look in the LaTeX code and cross reference the figure paths
with the `savefig` calls in the code.

## License

The License is MIT but don't forget to attribute/cite us. Copying without
proper citation will of course be considered plagiarism.
