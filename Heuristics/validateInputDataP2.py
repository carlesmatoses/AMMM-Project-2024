"""
AMMM Lab Heuristics
Instance file validator v2.0
Copyright 2020 Luis Velasco.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from AMMMGlobals import AMMMException


# Validate instance attributes read from a DAT file.
# It validates the structure of the parameters read from the DAT file.
# It does not validate that the instance is feasible or not.
# Use Problem.checkInstance() function to validate the feasibility of the instance.
class ValidateInputData(object):
    @staticmethod
    def validate(data):
        # Validate that all input parameters were found
        for paramName in ['D', 'n', 'N', 'd', 'm']:
            if paramName not in data.__dict__:
                raise AMMMException('Parameter/Set(%s) not contained in Input Data' % str(paramName))

        # Validate d
        d = list(data.d)
        data.d = d
        if len(d) != data.N:
            raise AMMMException('d(%s) length is not equal to the number of members' % str(d))

        # Validate D
        D = data.D
        if not isinstance(D, int) or (D <= 0):
            raise AMMMException('D(%s) has to be a positive integer' % str(D))
        if D > len(list(d)):
            raise AMMMException('D(%s) has to be smaller or equal to the quantity of members' % str(D))
        
        # Validate n
        n = list(data.n)
        data.n = n
        if len(n) != D:
            raise AMMMException('n(%s) length is not equal to the number of departments' % str(n))
        
        # Validate N
        N = data.N
        if not isinstance(N, int) or (N <= 0):
            raise AMMMException('N(%s) has to be a positive integer' % str(N))
        if N != len(list(d)):
            raise AMMMException('N(%s) has to be equal to the quantity of members' % str(N))


        # validate m
        m = list(data.m)
        for i in range(len(m)):
            m[i] = list(m[i])
        data.m = m
        
