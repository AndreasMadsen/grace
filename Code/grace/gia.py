# -*- coding: utf-8 -*-

import netCDF4 as nc
import os.path as path
import numpy as np
import load
import mpl_toolkits.basemap as maps
import matplotlib.pyplot as plt

thisdir = path.dirname(__file__)
dataset = nc.Dataset(path.join(thisdir, 'gia.nc'))

source_grid = np.asarray(dataset.variables['GIA_n100_mass_0km'])
source_lat = np.asarray(dataset.variables['Latitude'])
source_lon = np.asarray(dataset.variables['Longitude'])

## Rotate map to match GRACE data
(source_grid, source_lon) = maps.shiftgrid(180, source_grid, source_lon)
source_lon = source_lon - 360
#
## Flip the grid to match maps.interp requirements
source_lat = source_lat[::-1]
source_grid = source_grid[::-1, :]

(lons, lats) = (load.positions[:, :, 1], load.positions[:, :, 0])
# Unit convertion (from mm/yr to m/day)
grid = (source_grid / 1000) / (365.242)
