"""Defines the known initial values the emitter/receiver system."""

import numpy as np
from ..utils import io, error_handling, auxiliary

class System(object):
    def __init__(self,
                satellite_data_filepath,
                satellite_data_is_geographic_coords = True,
                satellite_data_scale_r = None,#1000.0,
                satellite_data_scale_velocity = None,#1.0/3.6
                r_emitter = None,
                TDoA_data = None,
                FDoA_data = None,
                n_sats = None,
                ):
        """
        Args:
            satellite_data_filepath: Complete filepath to the CSV file containing
                        satellite data (position, velocity, TDoA, etc.) 
            satellite_data_is_geographic_coords: Indicate if satellite positions are
                        provided in geographic coordinates (r, latitude, longitude).
            satellite_data_scale_r: If satellite radial coordinate is not meters,
                        provide a multiplying factor that will convert to meters.
            satellite_data_scale_velocity: If satellite velocity is not m/s,
                        provide a multiplying factor that will convert to m/s.
            r_emitter: If solving for a system with known emitter r coordinate
                        (radial distance from origin), provide it in meters. 
            TDoA_data: TDoA data, if it is not included in the satellite data CSV file.
            FDoA_data: TDoA data, if it is not included in the satellite data
            CSV file.
            n_sats: If specified, use only the first n satellites in calculation
        """

        # Load satellite (receiver) data.
        sat_data = io.load_csv_generic(filepath = satellite_data_filepath)
        if n_sats is not None:
            sat_data = sat_data.loc[:n_sats-1].reset_index(drop = True)
        # Scale/modify units if necessary. 
        sat_data = auxiliary.modify_sat_data_units(sat_data = sat_data, 
                            scale_r = satellite_data_scale_r, 
                            geographic_coords = satellite_data_is_geographic_coords, 
                            scale_velocity = satellite_data_scale_velocity)    

        # Ensure TDoA data is included.
        if (TDoA_data is None) and  \
                ('TDoA' not in sat_data.columns or sat_data.TDoA.isna().all()):
            raise error_handling.InsufficientDataError("TDoA must be provided.\n If emitter location is known, you can generate TDoA data with solver.verify.generate_TDoA() for testing.")
        elif TDoA_data is not None:
            # All TDoA including (d_(1,1) = 0) are given
            if (len(TDoA_data) == len(sat_data)) and (TDoA_data[0] == 0.0):
                sat_data['TDoA'] = TDoA_data
                self.TDoA_data = sat_data.TDoA.to_list()
            # All TDoA (d_(i,1), i !=1) are given. 
            elif len(TDoA_data)+1 == len(sat_data):
                sat_data['TDoA'] = np.zeros(len(sat_data))
                sat_data.loc[1:, 'TDoA'] = TDoA_data
                self.TDoA_data = sat_data.TDoA.to_list()
            # Unclear how to handle TDoA
            else:
                raise error_handling.UnknownCaseError("Unknown TDoA format.")


        # Check whether FDoA data exists.
        if (FDoA_data is None) and  \
                ('FDoA' not in sat_data.columns or sat_data.FDoA.isna().all()):
            print('System does not contain FDoA information.')
            self.FDoA_data = None
        elif FDoA_data is not None:
            # All FDoA including (\dot{d}_(1,1) = 0) are given
            if (len(FDoA_data) == len(sat_data)) and (FDoA_data[0] == 0.0):
                sat_data['FDoA'] = FDoA_data
                self.FDoA_data = sat_data.FDoA.to_list()
            # All FDoA (d_(i,1), i !=1) are given. 
            elif len(FDoA_data)+1 == len(sat_data):
                sat_data['FDoA'] = np.zeros(len(sat_data))
                sat_data.loc[1:, 'FDoA'] = FDoA_data
                self.FDoA_data = sat_data.FDoA.to_list()
            # Unclear how to handle FDoA
            else:
                raise error_handling.UnknownCaseError("Unknown FDoA format.")

        self.sat_data = sat_data
        self.r_emitter = r_emitter
    

         