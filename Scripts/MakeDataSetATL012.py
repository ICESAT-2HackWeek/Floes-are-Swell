
# ATL012 reader based on CC Bitz reader for ATL07. Reads an h5 file
# into an xArray data set
import warnings
warnings.filterwarnings('ignore')
#Import necesary modules
#Use shorter names (np, pd, plt) instead of full (numpy, pandas, matplotlib.pylot) for convenience
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pandas as pd
import numpy.ma as ma
import h5py
import s3fs
import matplotlib.pyplot as plt
import netCDF4
import xarray as xr

def MakeDataSetATL012(filename, beam='gt1r'):
    print(filename)
    ATL12 = h5py.File(filename, 'r')

    # coordinates, start their lives as data arrays
    lons = xr.DataArray(ATL12[beam+'/ssh_segments/longitude'][:],dims=['segs'])
    lons.name='lons'
    lats = xr.DataArray(ATL12[beam+'/ssh_segments/latitude'][:],dims=['segs'])
    lats.name='lats'
    # add 360 to lons less than 0
    lons360 = lons.where(lons.values>0, other=lons.values+360)

    # this is the time hacked a bit since I am an idiot, it is within seconds
    delta_time=ATL12[beam+'/ssh_segments/delta_time'][:] 
    time = np.datetime64('2018-01-01') + (delta_time-86400*0.015).astype('timedelta64[s]' ) 

    # variables in datasets, start their lives as data arrays too
    seg_dist = xr.DataArray(ATL12[beam+'/ssh_segments/stats/seg_dist_x_seg'][:],dims=['segs'])
    seg_dist.name = 'seg_dist' # the first two datarrays have to be named, grr
    #print(set_dist)

    h = xr.DataArray(ATL12[beam+'/ssh_segments/heights/h'][:],dims=['segs'])
    h.name = 'h'
    #print('\n\nTake a look at the dataarray we made \n')
    #print(height)
    swh = xr.DataArray(ATL12[beam+'/ssh_segments/heights/swh'][:],dims=['segs'])
    swh.name = 'swh'
    
    ssbias = xr.DataArray(ATL12[beam+'/ssh_segments/heights/bin_ssbias'][:],dims=['segs'])
    ssbias.name = 'ssbias'
       
    length_seg= xr.DataArray(ATL12[beam+'/ssh_segments/heights/length_seg'][:],dims=['segs'])
    # start by merging first two datarrays (they have to have names)
    ds=xr.merge([seg_dist, h])

    # now we add more dataarrays 
    ds['swh'] = swh
    ds['length_seg'] = length_seg
    
    ds.coords['lon'] = lons
    ds.coords['lat'] = lats
    ds.coords['time'] = xr.DataArray(time,dims=['segs'])
    ds.coords['delta_time'] = xr.DataArray(delta_time,dims=['segs'])

    ds.coords['lon360'] = lons360
    ds.coords['segs'] = xr.DataArray(np.arange(0,len(h),1),dims=['segs'])

    print('\n\nTake a look at the dataset we made \n')
    print(ds)

    return ds
