
__all__ = ["figure_dir", "figure_path"]

import os
import os.path as path
import sys

thisdir = path.dirname(path.realpath(__file__))
basedir = path.realpath(path.join(thisdir, '../'))

# Make it look like we are in the main code directory
sys.path.append(basedir)

# Resolve a figure_dir for `from setup import *`
figure_dir = path.realpath(path.join(basedir, '../Rapport/figures'))

# Validate that the figure_dir do exists
if (path.isdir(figure_dir) is False):
	raise OSError("figures directory not found (%s)" % (figure_dir))

def figure_path(name):
	return path.join(figure_dir, name)
