"""Auxiliary functions."""

import numpy as np
from . import conversion, earth_model

def modify_sat_data_units(sat_data = None,
                    scale_r = None,
                    geographic_coords = None,
                    scale_velocity = None):
    """
    Modify satellite data by converting to SI units, cartesian coordinates, and
    calculating local altitude (h). 
    """
    if scale_r is not None:
        sat_data.loc[:,'r'] = sat_data['r'] * scale_r
    if geographic_coords:
        r_local = earth_model.local_earth_radius(lat = sat_data.latitude, lon = sat_data.longitude)
        sat_data.loc[:,'h'] = sat_data['r'] - r_local 
        x, y, z = conversion.geographic2cartesian(lat = sat_data.latitude, lon = sat_data.longitude, h = sat_data.h)
        sat_data.loc[:,'x'] = x
        sat_data.loc[:,'y'] = y
        sat_data.loc[:,'z'] = z
    if scale_velocity is not None:
        sat_data.loc[:,'vx'] = sat_data['vx'] * scale_velocity 
        sat_data.loc[:,'vy'] = sat_data['vy'] * scale_velocity 
        sat_data.loc[:,'vz'] = sat_data['vz'] * scale_velocity 

    return sat_data
