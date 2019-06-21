#!/usr/bin/env python

# This code written by CC reads in data from an ATL07 dataset and then spits out an xarray
# data array. 
# There are two pieces of code: 
# readintoxr.MakeDataSet(LocalFilePath,beam)
# returns an xarray dataset for a given .h5 file and beam

# readintoxr.MultiFileDataSet(multiple_files, beams)
# returns an xarray dataset indexed by len(multiple_files) and len(beams)
# for multiple files and beams

import h5py
import numpy as np
import xarray as xr


def MakeDataSet(LocalFilePath, beam='gt1r'):
    ATL07 = h5py.File(LocalFilePath, 'r')

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
    ATL07 = None

    return ds

def MultiFileDataSet(multiple_files, beams):

    num_beams = np.size(beams) # do not use len !
    num_files = np.size(multiple_files)
    ds_beams = None
    ds_all = None
    file = None
    beam = None

    if num_files>1:

        ifile = 0
        for file in multiple_files:
            if num_beams>1:
                ibeams=0
                for beam in beams:
                    #print(beam)
                    ds = MakeDataSet(file, beam)
                    if ibeams==0:
                        ds_beams = ds
                    else:
                        ds_beams =xr.concat([ds, ds_beams])

                    ibeams = ibeams+1
                ds_beams = ds_beams.rename({'concat_dims':'beam'})
            else:
                ds_beams = MakeDataSet(file, beams)

            if ifile==0:
                ds_all = ds_beams
            else:
                ds_all =xr.concat([ds_beams, ds_all])
            ifile=ifile+1

    #    print(ds_all)
        ds_all = ds_all.rename({'concat_dims':'track'})
        ds_all.coords['track'] = xr.DataArray(np.arange(0,num_files,1),dims=['track'])
        if num_beams > 1:
            ds_all = ds_all.transpose('segs','track','beam')
            ds_all.coords['beam'] = xr.DataArray(np.arange(0,num_beams,1),dims=['beam'])

    else:
        # just one file
            if num_beams>1:
                ibeams=0
                for beam in beams:
                    #print(beam)
                    ds = MakeDataSet(multiple_files, beam)
                    if ibeams==0:
                        ds_beams = ds
                    else:
                        ds_beams =xr.concat([ds, ds_beams])

                    ibeams = ibeams+1
                ds_all = ds_beams.rename({'concat_dims':'beam'})
                ds_all.coords['beam'] = xr.DataArray(np.arange(0,num_beams,1),dims=['beam'])
            else:
                ds_all = MakeDataSet(multiple_files, beams)

    ds=None
    ds_beams = None

    return ds_all

