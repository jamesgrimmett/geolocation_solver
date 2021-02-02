"""
Run the example from Section VI of Ho & Chan (1997)
Here the emitter location is known in advance and we generate the TDOA's.
to verify the accuracy of the solution.
"""

import os
from geolocation.solver import verify, solver, system
from geolocation.utils import io, auxiliary

r_emitter = 6367287.0 # meters
lat_emitter = 45.35
lon_emitter = 75.9

dir = os.path.abspath(os.path.dirname(__file__))

def main():
    # Load satellite (receiver) data.
    sat_data = io.load_csv_generic(filepath = './data/example_satellites.csv')

    # No. satellite measurements > 3 is not currently implemented
    sat_data = sat_data.loc[:2].reset_index(drop = True)

    # Scale/modify units. 
    sat_data = auxiliary.modify_sat_data_units(sat_data = sat_data, 
                        geographic_coords = True,
                        scale_r = 1000.0, 
                        scale_velocity = 1.0/3.6)    


    tdoa = verify.generate_TDOA(sat_data = sat_data, 
                r_emitter = r_emitter,
                lat_emitter = lat_emitter,
                lon_emitter = lon_emitter,
                tdoa_var = 1.e-10)

    sys = system.System(satellite_data_filepath = './data/example_satellites.csv',
                        satellite_data_scale_r = 1000.0,
                        satellite_data_scale_velocity = 1.0/3.6,
                        r_emitter = r_emitter,
                        TDoA_data = tdoa,
                        n_sats = 3,
                        )

    s = solver.Solver(sys) 

    s.TDoA_solve()


if __name__ == '__main__':
    main()
