# geolocation_solver
Geolocation using TDOA and FDOA.

The geolocation solution outlined by [Ho & Chan (1997)](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=599239) is implemented in Python.
This algorithm can solve for the location of an emitter with a *known altitude*, given the TDOA alone, or in combination with the FDOA, of the signal recieved by at least three satellites. The location and velocity of the satellites must also be known.  
