
__all__ = ['time_epoch', 'date_to_days', 'days_to_date', 'days_to_str']

import numpy as np

time_epoch = np.datetime64('2007-08-07')

def date_to_days(ndarray):
	relative = ndarray.astype('datetime64[D]') - time_epoch
	return relative.astype('timedelta64[D]').astype('int')

def days_to_date(ndarray):
	absolute = time_epoch + ndarray.astype('timedelta64[D]')
	return absolute.astype('datetime64[D]')

def days_to_str(ndarray):
	return days_to_date(ndarray).astype('str')
