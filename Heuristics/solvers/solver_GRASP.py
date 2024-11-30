'''
AMMM Lab Heuristics
GRASP solver
Copyright 2018 Luis Velasco.

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
'''

import random
import time
from solver import _Solver
from solvers.localSearch import LocalSearch


# Inherits from the parent abstract solver.
class Solver_GRASP(_Solver):

    def _selectCandidate(self, candidateList, alpha):

        # sort candidate assignments by highestLoad in ascending order
        sortedCandidateList = sorted(candidateList, key=lambda x: x.highestLoad)
        
        # compute boundary highest load as a function of the minimum and maximum highest loads and the alpha parameter
        minHLoad = sortedCandidateList[0].highestLoad
        maxHLoad = sortedCandidateList[-1].highestLoad
        boundaryHLoad = minHLoad + (maxHLoad - minHLoad) * alpha
        
        # find elements that fall into the RCL
        maxIndex = 0
        for candidate in sortedCandidateList:
            if candidate.highestLoad <= boundaryHLoad:
                maxIndex += 1

        # create RCL and pick an element randomly
        rcl = sortedCandidateList[0:maxIndex]          # pick first maxIndex elements starting from element 0
        if not rcl: return None
        return random.choice(rcl)          # pick a candidate from rcl at random
    
    def _greedyRandomizedConstruction(self, alpha):
        # get an empty solution for the problem
        solution = self.instance.createSolution()
        
        # get members and sort them by their total affinity in descending order
        # members = self.instance.getMembers()
        # sortedMembers = sorted(members, key=lambda t: t.getWeight(), reverse=True)

        # for each member taken in sorted order
        for i in range(0, self.numMembers):
            
            # compute feasible assignments
            candidateList = solution.findFeasibleAssignments()

            # no candidate assignments => no feasible assignment found
            if not candidateList:
                # solution.makeInfeasible()
                break
            
            # select an assignment
            candidate = random.choice(candidateList)#self._selectCandidate(candidateList, alpha)

            # assign the current task to the CPU that resulted in a minimum highest load
            solution.assign(candidate.memberId)
            
        return solution
    
    def stopCriteria(self):
        self.elapsedEvalTime = time.time() - self.startTime
        return time.time() - self.startTime > self.config.maxExecTime

    def solve(self, **kwargs):
        self.startTimeMeasure()
        incumbent = self.instance.createSolution() # return Solution object
        incumbent.makeInfeasible()
        bestCompatibility = incumbent.getFitness()
        self.numMembers = self.instance.getNumMembers()
        self.writeLogLine(bestCompatibility, 0)

        iteration = 0
        last_time_check = time.time()
        while not self.stopCriteria():
            iteration += 1
            
            if iteration % 1000 == 0:
                current_time = time.time()
                elapsed_time = current_time - last_time_check
                print(f"Elapsed time for {iteration} iterations: {elapsed_time} seconds")
                last_time_check = current_time
                
            if iteration > 10000:
                break
            
            # force first iteration as a Greedy execution (alpha == 0)
            alpha = 0 if iteration == 1 else self.config.alpha

            solution = self._greedyRandomizedConstruction(alpha)
            # TODO: implement local search
            # if self.config.localSearch:
            #     localSearch = LocalSearch(self.config, None)
            #     endTime = self.startTime + self.config.maxExecTime
            #     solution = localSearch.solve(solution=solution, startTime=self.startTime, endTime=endTime)

            if solution.isFeasible():
                # solution.updateFitness()
                solutionObjective = solution.getFitness()
                if solutionObjective > bestCompatibility :
                    incumbent = solution
                    bestCompatibility = solutionObjective
                    self.writeLogLine(bestCompatibility, iteration)

        self.writeLogLine(bestCompatibility, iteration)
        self.numSolutionsConstructed = iteration
        self.printPerformance()
        return incumbent

