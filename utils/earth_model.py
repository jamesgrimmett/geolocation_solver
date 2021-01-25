"""Utils for Earth model. Assumed to be an oblate spheroid."""

# Equatorial radius
r_e = 6378137.0
# Eccentricity
ecc = = 0.0818191908426214957
# Polar radius

def local_earth_radius(lat, lon):
    """
    The local Earth radius for given latitude and longitude.
    
    Args:
        lat: Latitude in degrees (neg. south) [-90,90]
        lon: Longitude in degrees (neg. west) [-180,180]
    Returns:
        r: The local Earth radius in meters.
    """

    lat = geodetic_latitude(lat)

    gamma = r_e / np.sqrt(1 - ecc**2 * np.sin(lat)**2)
    
    x = gamma * np.cos(lat) * np.cos(lon)
    y = gamma * np.cos(lat) * np.sin(lon)
    z = (1 - ecc**2) * gamma * np.sin(lat)

    r = np.sqrt(x**2 + y**2 + z**2)

    return r

def geodetic_latitude(lat):
    """
    Converts geographic latitude to geodetic latitude.
    Eq. 58 of Ho & Chan (1997).
    """

    geod_lat = np.arctan( np.tan(lat) / (1 - ecc**2) )
    
    return geod_lat

