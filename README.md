# geolocation_solver
Multilateration solver for the geolocation of an emitting object given the TDoA alone, or in combination with FDoA, of the signal measured by multiple recievers. Implemented in Python.

Solvers:

| Algorithm         | Constraints                                                                       | Notes                                     | Status        |
| -------------     | --------------------------------------------------------------------------------- | ----------------------------------------- | ------------- |
| TDoA algorithm[1] | Emitter altitude must be known (can be zero). Limited to max. 3 receivers.        | Will be extended to allow > 3 recievers   | Functional    |
| FDoA algorithm[1] | Emitter altitude must be known (can be zero). Satellite velocities must be known. |                                           | In-progress   |
| Least squares     |                                                                                   |                                           | Planned       |

[1] The geolocation solution outlined by [Ho & Chan (1997)](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=599239).

## Usage example
Simple example using the data given in the example from Section VI of Ho & Chan
(1997). With a known emitter location and three receivers, generate TDoA data
and re-calculate the emitter location. 
```python
  from geolocation.solver import verify, solver, system
  from geolocation.utils import earth_model
  # Emitter location
  h_emitter = 0.0 # meters above sea level
  lat_emitter = 45.35
  lon_emitter = 75.9
  # Satellite locations
  sat_r = [42164, 42164, 42164] #km
  sat_lat = [2.0, 0.0, 0.0]
  sat_lon = [-50.0, -47.0, -53.0]
  # dummy tdoa  
  tdoa = [0.0, 0.0, 0.0]
 
  # Find emitter distance from origin
  r = earth_model.local_earth_radius(lat = lat_emitter, lon = lon_emitter)
  r_emitter = r - h_emitter
  # Pass satellite data and dummy TDoA to set sat_data dataframe and convert units.
  sys = system.System(satellite_positions = np.array([sat_r,sat_lat,sat_lon]).T,
                        is_geographic_coords = True,
                        r_emitter = r_emitter,
                        TDoA_data = tdoa,
                        scale_distance = 1000.0, 
                        )

  sat_data = sys.sat_data

  # Generate TDoA data using the known emitter location and 
  # some assumed measurement error
  tdoa = verify.generate_TDOA(sat_data = sat_data, 
              r_emitter = r_emitter,
              lat_emitter = lat_emitter,
              lon_emitter = lon_emitter,
              tdoa_var = 1.e-11)

  # Reinitialise the system with new TDoA data
  sys = system.System(satellite_positions = np.array(sat_data[['r','latitude','longitude']]),
                      is_geographic_coords = True,
                      r_emitter = r_emitter,
                      TDoA_data = tdoa,
                      )

  # Solve.
  s = solver.Solver(sys) 
  s.TDoA_solve()
```