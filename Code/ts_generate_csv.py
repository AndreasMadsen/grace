

import grace.ols
import numpy as np

initial = (26, 130)

(y, days) = grace.ols.interpolate(initial[0], initial[1])

np.savetxt("ts_greenland.csv", y, delimiter=",")
