
import load
import numpy as np
import mpl_toolkits.basemap as maps

def mask_matrix():
	(lons, lats) = (load.positions[:, :, 1], load.positions[:, :, 0])
	mask = np.ones_like(load.positions[:, :, 0])
	mask = maps.maskoceans(lons, lats, mask, inlands=False)
	mask = np.ma.filled(mask, 0)
	return mask.astype('bool')
