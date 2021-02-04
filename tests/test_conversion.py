"""Test conversion functions."""

from geolocation.utils import conversion, earth_model

x_test = earth_model.r_e
y_test = 0
z_test = 0

lat_test = 0
lon_test = 0
h_test = 0

def test_cartesian2geographic():
    lat,lon,h = conversion.cartesian2geographic(x = x_test, y = y_test, z = z_test)
    assert lat == lat_test
    assert lon == lon_test
    assert h == h_test

def test_geographic2cartesian():
    x, y, z = conversion.geographic2cartesian(lat = lat_test, lon = lon_test, h = h_test)
    assert x == x_test
    assert y == y_test
    assert z == z_test
