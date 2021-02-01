"""
Run the example from Section VI of Ho & Chan (1997)
Here the emitter location is known in advance and we generate the TDOA's.
to verify the accuracy of the solution.
"""

import os
from geolocation.solver import verify, solver
from geolocation.utils import io, auxiliary

r_emitter = 6367287.0 # meters
lat_emitter = 45.35
lon_emitter = 75.9

dir = os.path.abspath(os.path.dirname(__file__))

def main():
    sat_data = io.load_csv_generic(filepath = './data/example_satellites.csv')

    # No. satellite measurements > 3 is not currently implemented
    sat_data = sat_data.loc[:2].reset_index(drop = True)

    sat_data = auxiliary.modify_sat_data_units(sat_data = sat_data, 
                                        r_is_km = True, 
                                        geographic_coords = True, 
                                        velocity_is_kmh = True)    

    tdoa = verify.generate_TDOA(sat_data = sat_data, 
                r_emitter = r_emitter,
                lat_emitter = lat_emitter,
                lon_emitter = lon_emitter,
                tdoa_var = 1.e-10)

    s = solver.TDOASolver(r_emitter = r_emitter, 
                                sat_data = sat_data,
                                TDOA_data = tdoa)

    s.solve()


if __name__ == '__main__':
    main()
