
__all__ = ["autobuild", "generate", "reset"]

import source
import os
import os.path as path
import sqlite3 as sqlite
import numpy as np
import timeit

# Resolve absolute directory path to the numpy files
grids_file = path.join(path.dirname(path.realpath(__file__)), 'grids.npy');
dates_file = path.join(path.dirname(path.realpath(__file__)), 'dates.npy');
positions_file = path.join(path.dirname(path.realpath(__file__)), 'positions.npy');

def autobuild():
	if (path.isfile(grids_file) == False or path.isfile(dates_file) == False or path.isfile(positions_file) == False):
		print "build datafiles for the first time"
		generate()
		print "datafiles build"

def generate():
	"""
	Build a two numpy arrays one for grids and one for dates and save both to
	disk at grids.npy and dates.npy
	"""
	# grids and dates
	grids = np.empty((180, 360, 341), dtype='float32')
	dates = np.empty((341, 2), dtype='datetime64[D]')

	for index, name in enumerate(source.filelist):
		grids[:,:,index] = source.getgrid(name)
		dates[index,:] = source.getdate(name)

	# positions
	positions = np.empty((180, 360, 2), dtype='float32')

	for lat in range(0, 180):
		for lon in range(0, 360):
			positions[lat, lon, :] = source.getposition((lat, lon))

	# Save to disk
	np.save(grids_file, grids)
	np.save(dates_file, dates)
	np.save(positions_file, positions)

def reset():
	"""
	Removes the numpy file, meaning grids.npy
	"""
	if (path.isfile(grids_file)): os.unlink(grids_file)
	if (path.isfile(dates_file)): os.unlink(dates_file)
	if (path.isfile(positions_file)): os.unlink(positions_file)

if __name__ == "__main__":
	reset()
	autobuild()
	assert np.load(grids_file).shape == (180, 360, 341)
	assert np.load(dates_file).shape == (341, 2)
	assert np.load(positions_file).shape == (180, 360, 2)
	print "numpy file build"
