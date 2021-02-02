"""Solves the system of equations to find emitter location."""

import os
import pandas as pd
import numpy as np
from . import verify
from ..utils import constants, io, error_handling


class Solver(object):
    def __init__(self,
                system,
                ):
        """
        Args:
            system: Instance of the System class, containing information about the
                    system to be solved (receiver positions, TDoA, FDoA, etc.)
        """

        self.system = system

    def solve(self):
        """
        Generic solve. The solution algorithm appropriate for the available data
        will be carried out.
        """

        system = self.system
        sat_data = system.sat_data
        m = len(sat_data)

        G1 = self.populate_G1()
        h = self.populate_h()

        # TDoA only
        if (system.TDoA_data is not None and 
                system.FDoA_data is None): 
            if m == 3: 
                G1_inv = np.linalg.inv(G1)
                G1_inv_h = np.matmul(G1_inv,h)
                coeffs = self.get_r1_coefficients(G1_inv_h = G1_inv_h)
                roots = np.roots(coeffs)
                roots = roots[roots > 0]
                state = np.transpose([[1, r1, r1**2] for r1 in roots])
                solution = np.transpose(np.matmul(G1_inv_h, state))
                error = verify.solution_error(sat_data = sat_data, roots = roots, solution = solution, tdoa = system.TDoA_data)
                self._print_solution(solution, roots, error)
                
                return roots, solution

            elif m >= 4: 
                raise error_handling.NotImplementedError()

        # T/FDoA
        elif (system.TDoA_data is not None and
                system.FDoA_data is not None):
            if m == 2:
                raise error_handling.NotImplementedError()
            elif m >= 3:# >=2 ?
                raise error_handling.NotImplementedError()

        else:
            raise error_handling.UnknownCaseError(
                "TDOA solution requires measurements from at least 3 satellites.\nT/FDOA solution requires measurements from at least 2 satellites")


    def TDoA_solve(self):
        """
        Solve the system for the emitter location using only TDoA. If it exists,
        the FDoA information will be ignored.
        """

        system = self.system
        sat_data = system.sat_data
        m = len(sat_data)

        # If FDoA exists, remove it for now (restored at the end of function)
        if system.FDoA_data is not None:
            system.FDoA_data = None
            self.system = system
        
        G1 = self.populate_G1()
        h = self.populate_h()

        if m == 3: 
            G1_inv = np.linalg.inv(G1)
            G1_inv_h = np.matmul(G1_inv,h)
            coeffs = self.get_r1_coefficients(G1_inv_h = G1_inv_h)
            roots = np.roots(coeffs)
            roots = roots[roots > 0]
            state = np.transpose([[1, r1, r1**2] for r1 in roots])
            solution = np.transpose(np.matmul(G1_inv_h, state))
            error = verify.solution_error(sat_data = sat_data, roots = roots, solution = solution, tdoa = system.TDoA_data)
            self._print_solution(solution, roots, error) 

            return roots, solution

        elif m >= 4: 
            raise error_handling.NotImplementedError()


        else:
            raise error_handling.UnknownCaseError(
                "TDoA solution requires measurements from at least 3 satellites")

        # Restore the FDoA information to the system instance
        self._reset_system_attrs()


    def populate_G1(self):
        """
        """

        system = self.system
        sat_data = system.sat_data
        m = len(sat_data)

        if (system.TDoA_data is not None and 
                system.FDoA_data is None): 
            if m == 3: 

                s1 = np.array(sat_data.loc[0][['x','y','z']])
                s2_1 = np.array(sat_data.loc[1][['x','y','z']]) - s1
                s3_1 = np.array(sat_data.loc[2][['x','y','z']]) - s1

                G1 = np.array([s1, s2_1, s3_1])

            elif m >= 4: 

                s1 = np.array(sat_data.loc[0][['x','y','z']])
                G1 = np.array([d[['x','y','z']] - s1 for _,d in sat_data.loc[1:].iterrows()])

        elif (system.TDoA_data is not None and
                system.FDoA_data is not None):
            if m == 2:

                s1 = np.array(sat_data.loc[0][['x','y','z']])
                sdot1 = np.array(sat_data.loc[0][['vx','vy','vz']])
                s2_1 = np.array(sat_data.loc[1][['x','y','z']]) - s1
                sdot3_1 = np.array(sat_data.loc[1][['vx','vy','vz']]) - sdot1

                G1 = np.array([s1, s2_1, sdot3_1])

            elif m >= 3:# >=2 ?

                s1 = np.array(sat_data.loc[0][['x','y','z']])
                sdot1 = np.array(sat_data.loc[0][['vx','vy','vz']])
                G1_1 = np.array([d[['x','y','z']] - s1 for _,d in sat_data.loc[1:].iterrows()])
                G1_2 = np.array([d[['vx','vy','vz']] - sdot1 for _,d in sat_data.loc[1:].iterrows()])

                G1 = np.concatenate((G1_1,G1_2))

        else:

            raise error_handling.UnknownCaseError(
                "TDOA solution requires measurements from at least 3 satellites.\nT/FDOA solution requires measurements from at least 2 satellites")

        return -2 * G1


    def populate_h(self):
        """
        """ 

        system = self.system
        sat_data = system.sat_data
        m = len(sat_data)

        # TDoA 
        if (system.TDoA_data is not None and 
                system.FDoA_data is None):

            if m == 3: 

                if system.r_emitter is not None:
                    s1 = np.array(sat_data.loc[0][['x','y','z']])
                    s2 = np.array(sat_data.loc[1][['x','y','z']])
                    s3 = np.array(sat_data.loc[2][['x','y','z']])
                    s1sq = np.sum(s1**2)
                    s2sq = np.sum(s2**2)
                    s3sq = np.sum(s3**2)
                    d2_1 = sat_data.loc[1].TDoA * constants.speed_of_light
                    d3_1 = sat_data.loc[2].TDoA * constants.speed_of_light

                    h1 = np.array([-system.r_emitter**2 - s1sq, 0, 1])
                    h2 = np.array([d2_1**2 - s2sq + s1sq, 2 * d2_1, 0])
                    h3 = np.array([d3_1**2 - s3sq + s1sq, 2 * d3_1, 0])
                    h = np.array([h1, h2, h3])
                else:
                    error_handling.UnknownCaseError("Solution for unknown r_emitter is not yet implemented")

            elif m >= 4: 

                s1 = np.array(sat_data.loc[0][['x','y','z']])
                s1sq = np.sum(s1**2)
                h = np.array([(d.TDoA * constants.speed_of_light)**2 - np.sum(d[['x','y','z']]**2) + s1sq for i,d in sat_data.loc[1:].iterrows()])

        # T/FDOA        
        elif (system.TDoA_data is not None and
                system.FDoA_data is not None):
            if m == 2:

                error_handling.UnknownCaseError("Solution for T/FDOA is not yet implemented")

            elif m >= 3:# >=2 ?

                error_handling.UnknownCaseError("Solution for T/FDOA is not yet implemented")

        else:

            raise error_handling.UnknownCaseError(
                "TDOA solution requires measurements from at least 3 satellites.\nT/FDOA solution requires measurements from at least 2 satellites")

        return h


    def get_r1_coefficients(self, G1_inv_h):
        """
        """ 

        system = self.system
        sat_data = system.sat_data
        m = len(sat_data)

        # TDoA only
        if (system.TDoA_data is not None and 
                system.FDoA_data is None): 
            if m == 3: 

                if system.r_emitter is not None:
                    c0 = G1_inv_h[0,0]**2  + G1_inv_h[1,0]**2 +     \
                            G1_inv_h[2,0]**2  - system.r_emitter**2            
                    c1 = 2 * ( G1_inv_h[0,0] * G1_inv_h[0,1] +      \
                                G1_inv_h[1,0] * G1_inv_h[1,1] +     \
                                G1_inv_h[2,0] * G1_inv_h[2,1] )
                    c2 = G1_inv_h[0,1]**2 + G1_inv_h[1,1]**2 +      \
                            G1_inv_h[2,1]**2 +                      \
                            2 * (G1_inv_h[0,0] * G1_inv_h[0,2] +    \
                            G1_inv_h[1,0] * G1_inv_h[1,2] +         \
                            G1_inv_h[2,0] * G1_inv_h[2,2])
                    c3 = 2 * ( G1_inv_h[0,1] * G1_inv_h[0,2] +      \
                                G1_inv_h[1,1] * G1_inv_h[1,2] +     \
                                G1_inv_h[2,1] * G1_inv_h[2,2] )
                    c4 = G1_inv_h[0,2]**2 + G1_inv_h[1,2]**2 +      \
                            G1_inv_h[2,2]**2

                    return [c4, c3, c2, c1, c0]

                else:
                    error_handling.NotImplementedError()

            elif m >= 4: 
                error_handling.NotImplementedError()
        # T/FDoA
        elif (system.TDoA_data is not None and
                system.FDoA_data is not None):
            if m == 2:
                raise error_handling.NotImplementedError()
            elif m >= 3:# >=2 ?
                raise error_handling.NotImplementedError()

        else:
            raise error_handling.UnknownCaseError(
                "TDOA solution requires measurements from at least 3 satellites.\nT/FDOA solution requires measurements from at least 2 satellites")


    def _reset_system_attrs(self):
        """
        Reset the self.system attributes if they have been manipulated during solving.
        """

        system = self.system
        sat_data = system.sat_data

        # if FDoA data exists, reset the system.FDoA attribute.
        if (system.FDoA_data is None) and  \
                ('FDoA' in sat_data.columns and sat_data.FDoA.notna().any()):
            system.FDoA_data = sat_data.FDoA.to_list()

        self.system = system


    def _print_solution(self, solution, roots, error):
        """
        Print the solution for the emitter location.
        
        Args:
            solution: The emitter position [x,y,z] in meters
            roots: The possible solutions for r1 in meters
            error: The error in the solution.
        """
        print(f"{len(solution)} solution/s found:\n")
        newline = "\n"  # \escapes are not allowed inside f-strings
        #print(f'{newline.join(f"{s}" for s in solution)}')     
        strs = ["x: " + str(s[0]) + " m,\n" + "y: " + str(s[1]) + " m,\n" + "z: " + str(s[2]) + " m.\n" for s in solution] 
        #print(f'{newline.join(f"{s}" for s in strs)}')
        for i, s in enumerate(solution):
            print(f"Solution #{i}:\n")
            print(strs[i])
            print(f"TDoA relative error (max.): {np.max(error[i])}\n\n")

