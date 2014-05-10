# -*- coding: utf-8 -*-

__all__ = ["basedir", "figure_dir", "figure_path", "latexity"]

import os
import os.path as path
import sys
import re

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

def latexity(string):
	output = string \
		.replace('(t)', 't') \
		.replace(u'π', '\\pi') \
		.replace('cos', '\\cos') \
		.replace('sin', '\\sin') \
		.replace('*', '\\cdot')
	output = re.sub(r'([0-9A-Za-z\\.]+)/([0-9A-Za-z\\.]+)', r'\\frac{\1}{\2}', output)
	output = re.sub(r'([0-9])e([-0-9]+)', r'\1 \\cdot e^{\2}', output)
	return output
