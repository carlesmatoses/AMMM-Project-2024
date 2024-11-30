"""
AMMM Lab Heuristics
Representation of a problem instance
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

from problem.Member import Member
from problem.Department import Department
from problem.solution import Solution


class Instance(object):
    def __init__(self, config, inputData):
        self.config = config
        self.inputData = inputData
        self.D = inputData.D
        self.N = inputData.N
        self.d = inputData.d
        self.n = inputData.n
        self.m = inputData.m

        # TODO: Generate auxiliar classes
        self.members = [None] * self.N  # vector with members
        for nId in range(0, self.N):  # nId = 0..(N-1)
            self.members[nId] = Member(nId, self.d[nId]-1, self.m[nId])

        self.departments = [None] * self.D
        for dId in range(0, self.D):
            self.departments[dId] = Department(dId, self.n[dId])
            
    def getNumMembers(self):
        return self.N

    def getNumDepartments(self):
        return self.D

    def getMembers(self):
        return self.members

    def getDepartments(self):
        return self.n
    
    def getCompatibilityMatrix(self):
        return self.m
    
    def createSolution(self):
        # TODO: initate the solution with the auxiliar classes
        solution = Solution(self.members, [Department(dId, self.n[dId]) for dId in range(0, self.D)])
        solution.setVerbose(self.config.verbose)
        return solution

    def checkInstance(self):
        # TODO: Add checks to verify if the instance is feasible

        return True
