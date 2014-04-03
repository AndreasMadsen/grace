
__all__ = ["filelist", "getgrid", "getdata", "getposition"]

import os
import os.path as path
import csv
import datetime
import numpy as np

# Resolve the absolute directory path the grids directory
grids = path.join(path.dirname(path.realpath(__file__)), 'grids')

# Generate a list of all names for the datafiles in the grids directory
# nor the directory path or the file extension is a part of the final
# name
filelist = []
for name in os.listdir(grids):
	filepath = path.join(grids, name)
	if path.isdir(filepath) or (name[0] == '.') or ('\r' in filepath): continue
	filelist.append(os.path.splitext(name)[0])

def julian2date(julian):
	"""
	Return a python date object from a julian date given as an int.
	"""
	dt = datetime.timedelta(julian - 18262)
	return datetime.date(2000, 01, 01) + dt;

def getdate(name):
	"""
	Return two python dates as a tuple from the given datafile name,
	first is the start day, last is the end day.
	"""
	start = int(name[-11:-6])
	end = int(name[-5:])
	return (julian2date(start), julian2date(end))

def getgrid(name):
	"""
	Return a numpy array with the shape (180, 360). The index is then
	mat[latitude, longitude]

	Latitude is from +89.5 to -89.5
	Longitude is from -179.5 to +179.5
	"""
	filepath = path.join(grids, name + '.txt')
	reader = csv.reader(open(filepath), skipinitialspace=True, delimiter=" ")
	rows = [map(float, row) for row in reader]
	return np.asarray(rows).reshape((180, 360))

def getposition(index):
	"""
	Return (latitude, longitude) as a tuple from a truble containing
	the (row, collum) index associated with the numpy matrix meaning
	(latitudeIndex, longitudeIndex)
	"""
	if (index[0] < 0 or index[0] >= 180): raise LookupError('latitude index is out of range')
	if (index[1] < 0 or index[1] >= 360): raise LookupError('longitude index is out of range')

	return (89.5 - index[0], index[1] - 179.5)

if __name__ == "__main__":
	# test filelist
	assert len(filelist) == 341

	# test getdate
	assert map(str, getdate(filelist[0])) == ['2002-07-29', '2002-08-07']

	# test getdata
	assert getdata(filelist[0]).shape == (180, 360)

	# test getposition
	assert getposition((0  ,0  )) == (+89.5, -179.5)
	assert getposition((179,359)) == (-89.5, +179.5)

	print "all tests completed"
