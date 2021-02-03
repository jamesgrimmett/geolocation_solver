"""
Utils for converting coordinates / units.
"""

import numpy as np
from . import earth_model, error_handling

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

def cartesian2geographic(x, y, z):
    """
    Convert cartesian coordinates to geographic coordinates.

    Args:
        x: X geocentric coordinate (positive x-axis passing 
            through 0 degrees longitude at the equator).
        y: Y geocentric coordinate (positive y-axis passing
            through 90 degress longitude at the equator).
        z: Z geocentric coordinate (positive z-axis passing
            through north pole).
    
    Returns:
        lat: Latitude in degrees (neg. south) [-90,90]
        lon: Longitude in degrees (neg. west) [-180,180]
        h: Height in meters above the Earth's surface.
    """
    
    r_e = earth_model.r_e
    ecc = earth_model.ecc

    r = np.sqrt(x**2 + y**2 + z**2)
    p = np.sqrt(x**2 + y**2)
    f = np.roots([1,-2,ecc**2])
    #f = f[f <= 2][f >= 1]
    f = f[f>=0][f<=1]
    if len(f) > 1:
        raise error_handling.InvalidSolutionError("Unable to convert coordinates.")
    f = float(f)
    mu = np.arctan(z / p * ((1 - f) + ecc**2 * r_e / r) )
    lon = np.arctan(y / x)
    lat = np.arctan((z * (1-f) + ecc**2*r_e*np.sin(mu)**3) / ((1 - f) * (p - ecc**2*r_e*np.cos(mu)**3))) 
    
    lat = geodetic2geographic(lat)
    # Convert angles in degrees to radians
    lat = np.rad2deg(lat)
    lon = np.rad2deg(lon)

    local_r = earth_model.local_earth_radius(lat,lon)

    h = r - local_r

    return lat, lon, h   

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

def geodetic2geographic(geod_lat):
    """
    Converts geodetic latitude (radians) to geographic latitude (radians).
    Eq. 58 of Ho & Chan (1997).

    Args:
        lat: Geodetic latitude in degrees (neg. south) [-90,90]
    """

    ecc = earth_model.ecc
    lat = np.arctan( np.tan(geod_lat) * (1 - ecc**2) )
    
    return lat
