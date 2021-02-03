"""Defines the known initial values the emitter/receiver system."""

import numpy as np
import pandas as pd
from ..utils import io, error_handling, auxiliary

class System(object):
    def __init__(self,
                satellite_positions,
                is_geographic_coords,
                TDoA_data,
                satellite_velocities = None,
                FDoA_data = None,
                r_emitter = None,
                scale_distance = None,#1000.0,
                scale_velocity = None,#1.0/3.6
                ):
        """
        Args:
            satellite_positions: 3xn array of n satellite positions. Must be
                        either [r,latitude,longitude] or [x,y,z].
            is_geographic_coords: Indicate if satellite positions are
                        provided in geographic coordinates (r, latitude, longitude).
            TDoA_data: 1x(n-1) array of TDoA data for n-1 satellites relative to
                        first satellite. Can be 1xn if first element is zero.
            satellite_velocities: 3xn array of n satellite velocities. Must be
                        [vx,vy,vz]
            FDoA_data: 1x(n-1) array of FDoA data for n-1 satellites relative to
                        first satellite. Can be 1xn if first element is zero.
            r_emitter: If solving for a system with known emitter r coordinate
                        (radial distance from origin), provide it in meters. 
            scale_distance: If satellite coordinate data is not meters,
                        provide a multiplying factor that will convert to meters.
            scale_velocity: If satellite velocity is not m/s,
                        provide a multiplying factor that will convert to m/s.
        """

        cols = ['r','latitude','longitude','x','y','z','TDoA']
        sat_data = pd.DataFrame(np.zeros((len(satellite_positions), len(cols))), 
                                                                    columns = cols)

        # Fill satellite positional data
        if is_geographic_coords:
            sat_data['r'] = satellite_positions[:,0]
            sat_data['latitude'] = satellite_positions[:,1]
            sat_data['longitude'] = satellite_positions[:,2]
        else:
            sat_data['x'] = satellite_positions[:,0]
            sat_data['y'] = satellite_positions[:,1]
            sat_data['z'] = satellite_positions[:,2]

        # All TDoA including (d_(1,1) = 0) are given
        if (len(TDoA_data) == len(sat_data)) and (TDoA_data[0] == 0.0):
            sat_data['TDoA'] = TDoA_data
            self.TDoA_data = TDoA_data
        # All TDoA (d_(i,1), i !=1) are given. 
        elif len(TDoA_data)+1 == len(sat_data):
            sat_data['TDoA'] = np.zeros(len(sat_data))
            sat_data.loc[1:, 'TDoA'] = TDoA_data
            self.TDoA_data = sat_data.TDoA.to_list()
        # Unclear how to handle TDoA
        else:
            raise error_handling.UnknownCaseError("Unknown TDoA format.")


        # Check whether FDoA data exists.
        if FDoA_data is None:
            print('System does not contain FDoA information.')
            self.FDoA_data = None
        elif FDoA_data is not None:
            # All FDoA including (\dot{d}_(1,1) = 0) are given
            if (len(FDoA_data) == len(sat_data)) and (FDoA_data[0] == 0.0):
                sat_data['FDoA'] = FDoA_data
                self.FDoA_data = sat_data.FDoA_data
            # All FDoA (d_(i,1), i !=1) are given. 
            elif len(FDoA_data)+1 == len(sat_data):
                sat_data['FDoA'] = np.zeros(len(sat_data))
                sat_data.loc[1:, 'FDoA'] = FDoA_data
                self.FDoA_data = sat_data.FDoA.to_list()
            # Unclear how to handle FDoA
            else:
                raise error_handling.UnknownCaseError("Unknown FDoA format.")

            # Ensure velocity data is included
            if satellite_velocities is not None:
                sat_data['vx'] = satellite_velocities[:,0]
                sat_data['vy'] = satellite_velocities[:,1]
                sat_data['vz'] = satellite_velocities[:,2]
            else:
                raise error_handling.InsufficientDataError("If using FDoA in solution, satellite velocities must be provided.")

        # Scale/modify units if necessary. 
        sat_data = auxiliary.modify_sat_data_units(sat_data = sat_data, 
                            scale_distance = scale_distance, 
                            geographic_coords = is_geographic_coords, 
                            scale_velocity = scale_velocity)    

        self.sat_data = sat_data
        self.r_emitter = r_emitter
    

         