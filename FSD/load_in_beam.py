#!/usr/bin/env python
import h5py
import xarray as xr
import numpy as np

#Import necesary modules
#Use shorter names (np, pd, plt) instead of full (numpy, pandas, matplotlib.pylot) for convenience
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import cartopy.crs as ccrs
# import pandas as pd
# import numpy.ma as ma

def read_beam(filename,beam):
    
    print(filename)
    ATL07 = h5py.File(filename, 'r')

    # coordinates, start their lives as data arrays
    lons = xr.DataArray(ATL07[beam+'/sea_ice_segments/longitude'][:],dims=['segs'])
    lons.name='lons'
    lats = xr.DataArray(ATL07[beam+'/sea_ice_segments/latitude'][:],dims=['segs'])
    lats.name='lats'
    # add 360 to lons less than 0
    lons360 = lons.where(lons.values>0, other=lons.values+360)

    # this is the time hacked a bit since I am an idiot, it is within seconds
    delta_time=ATL07[beam+'/sea_ice_segments/delta_time'][:] 
    time = np.datetime64('2018-01-01') + (delta_time-86400*0.015).astype('timedelta64[s]' ) 

    # variables in datasets, start their lives as data arrays too
    seg_dist = xr.DataArray(ATL07[beam+'/sea_ice_segments/seg_dist_x'][:],dims=['segs'])
    seg_dist.name = 'seg_dist' # the first two dataarrays have to be named, grr
    #print(set_dist)

    height = xr.DataArray(ATL07[beam+'/sea_ice_segments/heights/height_segment_height'][:],dims=['segs'])
    height.name = 'height'
    #print('\n\nTake a look at the dataarray we made \n')
    #print(height)
    
    mss = xr.DataArray(ATL07[beam+'/sea_ice_segments/geophysical/height_segment_mss'][:],dims=['segs'])
    seg_length= xr.DataArray(ATL07[beam+'/sea_ice_segments/heights/height_segment_length_seg'][:],dims=['segs'])
    quality_flag = xr.DataArray(ATL07[beam+'/sea_ice_segments/heights/height_segment_fit_quality_flag'][:],dims=['segs'])
    isita_lead =   xr.DataArray(ATL07[beam+'/sea_ice_segments/heights/height_segment_ssh_flag'][:],dims=['segs'])

    # start by merging first two datarrays (they have to have names)
    ds=xr.merge([seg_dist, height])

    # now we add more dataarrays 
    ds['mss'] = mss
    ds['seg_length'] = seg_length
    ds['quality_flag'] = quality_flag
    ds['isita_lead'] = isita_lead
    
    ds.coords['lon'] = lons
    ds.coords['lat'] = lats
    ds.coords['time'] = xr.DataArray(time,dims=['segs'])
    ds.coords['delta_time'] = xr.DataArray(delta_time,dims=['segs'])

    ds.coords['lon360'] = lons360
    ds.coords['segs'] = xr.DataArray(np.arange(0,len(height),1),dims=['segs'])

#    print('\n\nTake a look at the dataset we made \n')
#    print(ds)

    return ds

