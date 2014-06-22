# -*- coding: utf-8 -*-

import netCDF4 as nc
import os.path as path
import numpy as np
import load
import mpl_toolkits.basemap as maps

thisdir = path.dirname(__file__)
dataset = nc.Dataset(path.join(thisdir, 'gia.nc'))

source_grid = np.asarray(dataset.variables['Dsea_250'])
source_lat = np.asarray(dataset.variables['Lat'])
source_lon = np.asarray(dataset.variables['Lon'])

# Rotate map to match GRACE data
(source_grid, source_lon) = maps.shiftgrid(180, source_grid, source_lon)
source_lon = source_lon - 360

# Flip the grid to match maps.interp requirements
source_lat = source_lat[::-1]
source_grid = source_grid[::-1, :]

#
# Note the grid is stil half a degree of on the longitude.
# This is to fix that, by using a simple two dimentional interpolation.
#
(lons, lats) = (load.positions[:, :, 1], load.positions[:, :, 0])
grid = maps.interp(source_grid, source_lon, source_lat, lons, lats)

print grid
