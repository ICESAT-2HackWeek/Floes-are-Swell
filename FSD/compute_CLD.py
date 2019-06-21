#!/usr/bin/env python
import xarray as xr
import numpy as np

def get_CLD(beam_xarr):
    
    q = beam_xarr.isita_lead
    # print(len(q))


    startvec = np.concatenate([[0],q])
    endvec = np.concatenate([q, [0]])

    up = (startvec[:-1]==0) & (startvec[1:]==1)
    down = (endvec[:-1]==1) & (endvec[1:]==0)
    startind = np.concatenate(np.where(up==1))
    endind = np.concatenate(np.where(down==1))

    # Eliminate all which are isolated single ice measurements
    same = np.intersect1d(startind,endind)
    startind = np.setdiff1d(startind,same)
    endind = np.setdiff1d(endind,same)
    startind = startind - 1 # because we prepended a zero


    startx = beam_xarr.seg_dist[startind]
    startx = startx.drop(('lat','lon','time','delta_time','lon360','segs'))
    endx = beam_xarr.seg_dist[endind]
    endx = endx.drop(('lat','lon','time','delta_time','lon360','segs'))

    chord_lengths = endx - startx
        
    return chord_lengths


