"""
Run the example from Section VI of Ho & Chan (1997)
Here the emitter location is known in advance and we generate the TDOA's.
to verify the accuracy of the solution.
"""

from geolocation.solver import verify, solver, system
from geolocation.utils import earth_model

h_emitter = 0.0 # meters above sea level
lat_emitter = 45.35
lon_emitter = 75.9

#dir = os.path.abspath(os.path.dirname(__file__))

def main():
    # First three satellites from the example given in 
    # Section VI of Ho & Chan (1997) 
    sat_r = [42164, 42164, 42164] #km
    sat_lat = [2.0, 0.0, 0.0]
    sat_lon = [-50.0, -47.0, -53.0]
    # dummy tdoa 
    tdoa = [0.0, 0.0, 0.0]

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

    # Generate TDoA data using the known emitter location
    tdoa = verify.generate_TDOA(sat_data = sat_data, 
                r_emitter = r_emitter,
                lat_emitter = lat_emitter,
                lon_emitter = lon_emitter,
                tdoa_var = 1.e-11)

    # Reinitialise the system with actual TDoA
    sys = system.System(satellite_positions = np.array(sat_data[['r','latitude','longitude']]),
                        is_geographic_coords = True,
                        r_emitter = r_emitter,
                        TDoA_data = tdoa,
                        )

    # Solve.
    s = solver.Solver(sys) 
    s.TDoA_solve()


if __name__ == '__main__':
    main()
