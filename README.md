# geolocation_solver
Multilateration solver for the geolocation of an emitting object given the TDoA alone, or in combination with FDoA, of the signal measured by multiple recievers. Implemented in Python.

Solvers:

| Algorithm         | Constraints                                                                       | Notes                                     | Status        |
| -------------     | --------------------------------------------------------------------------------- | ----------------------------------------- | ------------- |
| TDoA algorithm[1] | Emitter altitude must be known (can be zero). Limited to max. 3 receivers.        | Will be extended to allow > 3 recievers   | Available     |
| FDoA algorithm[1] | Emitter altitude must be known (can be zero). Satellite velocities must be known. |                                           | In-progress   |
| Least squares     |                                                                                   |                                           | Planned       |
[1] The geolocation solution outlined by [Ho & Chan (1997)](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=599239).
