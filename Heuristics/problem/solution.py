"""
AMMM Lab Heuristics
Representation of a solution instance
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

import copy
import itertools
from solution import _Solution
from problem.Member import Member
from problem.Department import Department

# This class stores the load of the highest loaded CPU
# when a task is assigned to a CPU.
class Assignment(object):
    def __init__(self, member:int, weight:int=0):
        self.memberId = member
        self.weight = weight

    def __str__(self):
        return f"member: {self.memberId}"


# Solution includes functions to manage the solution, to perform feasibility
# checks and to dump the solution into a string or file.
class Solution(_Solution):
    def __init__(self, members:list[Member], departments:list[Department]):
        
        self.members = members
        self.departments = departments 
        # self.objective = 0
        # self.c = [0]*len(self.members)
        # self.x = [[0 for _ in range(self.N)] for _ in range(self.N)]
        
        self.committeeMembersSize = sum([d.maxCapacity for d in self.departments])
        self.committeeMembers:list[int] = []
        
        super().__init__()

    def isFeasible(self) -> bool:
        # check constraints
        pairs = list(itertools.combinations(self.committeeMembers, 2))
        
        # Constrain 1: All departments must have exactly the maxCapacity
        for department in self.departments:
            if department.currentCapacity != 0:
                return False
        
        # Constrain 2: There is no couple of member assigned with 0 compatibility
        for m1, m2 in pairs:
            if not self.members[m1].getCompatibility(m2):
                return False
            
        # Constrain 3: For each couple of members ni and nj with a compatibility lower than 0.15,
        # the solution must contain a member with a 0.85 compatibility with both ni and nj
        for m1, m2 in pairs:
            if self.members[m1].getCompatibilityValue(m2) < 0.15:
                found = False
                for m in self.committeeMembers:
                    if m != m1 and m != m2:
                        if (self.members[m].getCompatibilityValue(m1) >= 0.85 and
                            self.members[m].getCompatibilityValue(m2) >= 0.85):
                            found = True
                            break
                if not found:
                    return False
        
        # print department id, maximum capacity, current capacity and members
        # print(f"Department {department.getId()}:")
        # print(f"  max space     : {department.maxCapacity}")
        # print(f"  current space : {department.currentCapacity}")
        # print(f"  members       : {department.members}")
        
        return True
    
    def isFeasibleToAssignMemberToCommittee(self, member:int) -> bool:
        # check if committee is already full
        if len(self.committeeMembers) >= self.committeeMembersSize:
            return False
        
        # check if already selected
        if member in self.committeeMembers:
            return False
        
        # check if department capacity is already full
        memberInstance = self.members[member]
        if self.departments[memberInstance.getDepartmentID()].currentCapacity <= 0:
            return False
        
        # check if its incopatible with any other member
        for committeeMember in self.committeeMembers:
            if memberInstance.getCompatibility(committeeMember) == False:
                return False

        return True
    
    def updateFitness(self):
        pairs = list(itertools.combinations(self.committeeMembers, 2))
        total_compatibility = sum(self.members[m1].getCompatibilityValue(m2) for m1, m2 in pairs)
        average_compatibility = total_compatibility / (len(pairs)) if pairs else 0
        self.fitness = average_compatibility
    
    def assign(self, memberId:int)->bool:
        if not self.isFeasibleToAssignMemberToCommittee(memberId):return False

        self.committeeMembers.append(memberId)
        memberInstance = self.members[memberId]
        self.departments[memberInstance.getDepartmentID()].assignMember(memberId)
        
        # Calculate the average compatibility
        self.updateFitness()
        
        return True
  
    def unassign(self, memberId:int)->bool:
        # if not self.isFeasibleToUnassignTaskFromCPU(taskId, cpuId): return False

        self.committeeMembers.remove(memberId)
        memberInstance = self.members[memberId]
        self.departments[memberInstance.getDepartmentID()].unassignMember(memberId)
        
        self.updateFitness()
        
        return True
  
    def findFeasibleAssignments(self):
        feasibleAssignments:list[Assignment] = []
        for member in range(len(self.members)):
            feasible = self.assign(member)
            if not feasible: continue
            assignment = Assignment(member, self.members[member].getWeight())
            feasibleAssignments.append(assignment)

            self.unassign(member)

        return feasibleAssignments


    def __str__(self):
        strSolution =""
        strSolution += f"OBJECTIVE: {self.fitness}\n"
        strSolution += f"Commission: {' '.join(map(str, self.committeeMembers))}"
        return strSolution

