"""Auxiliary functions."""

import numpy as np
from . import conversion, earth_model

def modify_sat_data_units(sat_data = None,
                    r_is_km = None,
                    geographic_coords = None,
                    velocity_is_kmh = None):
    """
    Modify satellite data by converting to SI units, cartesian coordinates, and
    calculating local altitude (h). 
    """
    if r_is_km:
        sat_data.loc[:,'r'] = sat_data['r'] * 1000.0
    if geographic_coords:
        r_local = earth_model.local_earth_radius(lat = sat_data.latitude, lon = sat_data.longitude)
        sat_data.loc[:,'h'] = sat_data['r'] - r_local 
        x, y, z = conversion.geographic2cartesian(lat = sat_data.latitude, lon = sat_data.longitude, h = sat_data.h)
        sat_data.loc[:,'x'] = x
        sat_data.loc[:,'y'] = y
        sat_data.loc[:,'z'] = z
    if velocity_is_kmh:
        sat_data.loc[:,'vx'] = sat_data['vx'] / 3.6
        sat_data.loc[:,'vy'] = sat_data['vy'] / 3.6
        sat_data.loc[:,'vz'] = sat_data['vz'] / 3.6

    return sat_data

#def fill_emitter_distance(sat_data = None,
#                            r_emitter = None,
#                            lat_emitter = None,
#                            lon_emitter = None):
#
#    local_r_emitter = earth_model.local_earth_radius(lat = lat_emitter, lon = lon_emitter) 
#    h_emitter = r_emitter - local_r_emitter 
#    x_emitter, y_emitter, z_emitter = conversion.geographic2cartesian(lat = lat_emitter, lon = lon_emitter, h = h_emitter)
#    sat_data.loc[:,'d_emitter'] = np.sqrt((sat_data['x'] - x_emitter)**2 + 
#                                    (sat_data['y'] - y_emitter)**2 + 
#                                    (sat_data['z'] - z_emitter)**2)
#
#    return sat_data