"""
Utils for converting coordinates / units.
"""

import numpy as np
from . import earth_model

def geographic2cartesian(lat, lon, h = None, lat_is_geocentric = True):
    """
    Convert geographic coordinates to geocentric cartesian coordinates.

    Args:
        lat: Latitude in degrees (neg. south) [-90,90]
        lon: Longitude in degrees (neg. west) [-180,180]
        h: Height in meters above the Earth's surface.
        lat_is_geocentric: Boolean indicating whether the 
            given latitude is geocentric (False is geodetic)

    Returns:
        x: X geocentric coordinate (positive x-axis passing 
            through 0 degrees longitude at the equator).
        y: Y geocentric coordinate (positive y-axis passing
            through 90 degress longitude at the equator).
        z: Z geocentric coordinate (positive z-axis passing
            through north pole).
    
    """
    
    r_e = earth_model.r_e
    ecc = earth_model.ecc
    if h is None:
        h = 0.0

    # Convert angles in degrees to radians
    lat = np.deg2rad(lat)
    lon = np.deg2rad(lon)

    # Convert geographic latitude to geodetic latitude
    if lat_is_geocentric:
        lat = geographic2geodetic(lat)

    # Equations 57 - 59 in Ho & Chan (1997)
    gamma = r_e / np.sqrt(1 - ecc**2 * np.sin(lat)**2)
    
    x = (gamma + h) * np.cos(lat) * np.cos(lon)
    y = (gamma + h) * np.cos(lat) * np.sin(lon)
    z = ((1 - ecc**2) * gamma + h) * np.sin(lat)

    return x, y, z    

def geographic2geodetic(lat):
    """
    Converts geographic latitude (radians) to geodetic latitude (radians).
    Eq. 58 of Ho & Chan (1997).

    Args:
        lat: Latitude in degrees (neg. south) [-90,90]
    """

    ecc = earth_model.ecc
    geod_lat = np.arctan( np.tan(lat) / (1 - ecc**2) )
    
    return geod_lat
