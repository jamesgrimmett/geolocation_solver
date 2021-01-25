"""
Utils for converting coordinates / units.
"""

import numpy as np

def geographic2geocentric(lat, lon, el):
    """
    Convert geographic coordinates to geocentric cartesian coordinates.
    Assumes elevation is zero if not given, and the cartesian 'z' will 
    be returned as the local Earth radius.

    Args:
        lat: Latitude in degrees (neg. south) [-90,90]
        lon: Longitude in degrees (neg. west) [-180,180]
        el: Elevation in meters above the Earth's surface.
            Assumed 0 if None

    Returns:
        x: X geocentric coordinate (positive x-axis passing 
            through 0 degrees longitude at the equator).
        y: Y geocentric coordinate (positive y-axis passing
            through 90 degress longitude at the equator).
        z: Z geocentric coordinate (positive z-axis passing
            through north pole).
    
    """

    if el is None:
        el = local_earth_radius(lat, lon)

    

