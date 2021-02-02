import numpy as np
from ..utils import conversion, earth_model, constants, error_handling

def solution_error(sat_data = None,
                    roots = None, 
                    solution = None,
                    tdoa = None):
    """
    """
    sats = np.array(sat_data[['x','y','z']])
    tdoa_calc = np.array([
                    np.sqrt(np.sum((sats - s)**2, axis = 1)) - roots[i]     \
                    for i,s in enumerate(solution)]) / constants.speed_of_light

    # The TDOA to the first satellite should be zero
    if (abs(tdoa_calc[:,0]) > 1.e-12).any():
        print(f"roots: {roots}")
        print(f"solution: {solution}")
        raise error_handling.InvalidSolutionError()

    error = (tdoa_calc[:,1:] - tdoa[1:]) / tdoa[1:]

    return error
    

def generate_TDOA(sat_data = None, 
                r_emitter = None,
                lat_emitter = None,
                lon_emitter = None,
                tdoa_var = None):
    """
    """
    n_sats = len(sat_data)
    local_r_emitter = earth_model.local_earth_radius(lat = lat_emitter, lon = lon_emitter) 
    h_emitter = r_emitter - local_r_emitter 
    x_emitter, y_emitter, z_emitter = conversion.geographic2cartesian(lat = lat_emitter, lon = lon_emitter, h = h_emitter)
    d_emitter = np.sqrt((sat_data['x'] - x_emitter)**2 + 
                        (sat_data['y'] - y_emitter)**2 + 
                        (sat_data['z'] - z_emitter)**2)
    tdoa_clean = np.array([d_emitter[i] - d_emitter[0] for i in range(n_sats)]) / constants.speed_of_light 
    
    #if tdoa_var is None:
    #    tdoa_mean = np.mean(tdoa_clean)
    #    diff = tdoa_clean - tdoa_mean
    #    tdoa_var = np.matmul(diff, np.transpose(diff)) / (n_sats - 2)

    tdoa_noise = np.array(np.random.normal(loc = 0, 
                                       scale = np.sqrt(tdoa_var), 
                                       size = n_sats))
    tdoa_noise[0] = 0.0
    
    tdoa = tdoa_clean + tdoa_noise

    return tdoa
