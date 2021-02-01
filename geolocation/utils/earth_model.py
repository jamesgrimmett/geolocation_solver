"""Utils for Earth model. Assumed to be an oblate spheroid."""

import numpy as np
from . import conversion

# Equatorial radius
r_e = 6378137.0
# Eccentricity
ecc = 0.0818191908426214957

def local_earth_radius(lat, lon):
    """
    The local Earth radius for given latitude and longitude.
    
    Args:
        lat: Latitude in degrees (neg. south) [-90,90]
        lon: Longitude in degrees (neg. west) [-180,180]
    Returns:
        r: The local Earth radius in meters.
    """

    x, y, z = conversion.geographic2cartesian(lat,lon)

    r = np.sqrt(x**2 + y**2 + z**2)

    return r


