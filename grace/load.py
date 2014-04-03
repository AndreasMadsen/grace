
__all__ = ["grids", "dates", "positions"]

import os.path as path
import numpy as np
import timeit

# Resolve absolute directory path to the numpy files
grids_file = path.join(path.dirname(path.realpath(__file__)), 'grids.npy');
dates_file = path.join(path.dirname(path.realpath(__file__)), 'dates.npy');
positions_file = path.join(path.dirname(path.realpath(__file__)), 'positions.npy');

grids = np.load(grids_file)
dates = np.load(dates_file)
positions = np.load(positions_file)
