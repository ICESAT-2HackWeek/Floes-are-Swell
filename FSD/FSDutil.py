#!/usr/bin/env python
import xarray as xr
import numpy as np

def get_CLD(beam_xarr):
    
    isita_floe = 1 - beam_xarr.isita_lead

    startvec = np.concatenate([[0],isita_floe])
    endvec = np.concatenate([isita_floe, [0]])

    up = (startvec[:-1]==0) & (startvec[1:]==1)
    down = (endvec[:-1]==1) & (endvec[1:]==0)
    
    startind = np.concatenate(np.where(up==1))
    endind = np.concatenate(np.where(down==1))
    
    # print(len(startind))

    # Eliminate all which are isolated single ice measurements
    same = np.intersect1d(startind,endind)
    startind = np.setdiff1d(startind,same)
    endind = np.setdiff1d(endind,same)
    startind = startind - 1 # because we prepended a zero

    # print(len(startind))

    # Get the mean latitudes and longitudes of the chords
    startlat = beam_xarr.lat[startind]
    startlat = startlat.drop(('lon','time','delta_time','lon360','segs'))

    endlat = beam_xarr.lat[endind]
    endlat = endlat.drop(('lon','time','delta_time','lon360','segs'))
    
    chordlat = 0.5*(startlat+endlat)

    startlon = beam_xarr.lon[startind]
    startlon = startlon.drop(('lat','time','delta_time','lon360','segs'))

    endlon = beam_xarr.lon[endind]
    endlon = endlon.drop(('lat','time','delta_time','lon360','segs'))
    chordlon = 0.5*(startlon+endlon)
    
    startx = beam_xarr.seg_dist[startind]
    startx = startx.drop(('lat','lon','time','delta_time','lon360','segs'))
    endx = beam_xarr.seg_dist[endind]
    endx = endx.drop(('lat','lon','time','delta_time','lon360','segs'))

    chord_lengths = endx - startx
    
    goodL = chord_lengths > 0
    
    chord_lengths = chord_lengths[goodL]
    chordlat = chordlat[goodL]
    chordlon = chordlon[goodL]
    
    return chord_lengths,chordlat,chordlon

def get_LWD(beam_xarr):
    
    isita_lead = beam_xarr.isita_lead
    # print(len(q))

    startvec = np.concatenate([[0],isita_lead])
    endvec = np.concatenate([isita_lead, [0]])

    up = (startvec[:-1]==0) & (startvec[1:]==1)
    down = (endvec[:-1]==1) & (endvec[1:]==0)
    startind = np.concatenate(np.where(up==1))
    endind = np.concatenate(np.where(down==1))

    # Do not eliminate single lead measurements
    # same = np.intersect1d(startind,endind)
    # startind = np.setdiff1d(startind,same)
    # endind = np.setdiff1d(endind,same)
    startind = startind - 1 # because we prepended a zero

    # Get the mean latitudes and longitudes of the chords
    startlat = beam_xarr.lat[startind]
    startlat = startlat.drop(('lon','time','delta_time','lon360','segs'))

    endlat = beam_xarr.lat[endind]
    endlat = endlat.drop(('lon','time','delta_time','lon360','segs'))
    
    leadlat = 0.5*(startlat+endlat)

    startlon = beam_xarr.lon[startind]
    startlon = startlon.drop(('lat','time','delta_time','lon360','segs'))

    endlon = beam_xarr.lon[endind]
    endlon = endlon.drop(('lat','time','delta_time','lon360','segs'))
    leadlon = 0.5*(startlon+endlon)
    
    startx = beam_xarr.seg_dist[startind]
    startx = startx.drop(('lat','lon','time','delta_time','lon360','segs'))
    
    endx = beam_xarr.seg_dist[endind]
    endx = endx.drop(('lat','lon','time','delta_time','lon360','segs'))
    
    lead_widths = endx - startx
    
    goodL = lead_widths > 0

    lead_widths = lead_widths[goodL]
    leadlat = leadlat[goodL]
    leadlon = leadlon[goodL]
        
    return lead_widths,leadlat,leadlon

