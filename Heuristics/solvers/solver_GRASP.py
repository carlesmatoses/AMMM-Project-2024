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
        sortedCandidateList = sorted(candidateList, key=lambda x: x.weight, reverse=True)
        
        # compute boundary highest load as a function of the minimum and maximum highest loads and the alpha parameter
        minHWeight = sortedCandidateList[-1].weight
        maxHWeight = sortedCandidateList[0].weight
        boundaryHWeight = minHWeight + (maxHWeight - minHWeight) * alpha
        
        # find elements that fall into the RCL
        maxIndex = 0
        for candidate in sortedCandidateList:
            if candidate.weight >= boundaryHWeight:
                maxIndex += 1

        # create RCL and pick an element randomly
        rcl = sortedCandidateList[0:maxIndex] # pick first maxIndex elements starting from element 0
        if not rcl: return None
        return random.choice(rcl) # pick a candidate from rcl at random
    
    def _greedyRandomizedConstruction(self, iteration):
        """Construction phase of the GRASP algorithm."""
        # get an empty solution for the problem
        solution = self.instance.createSolution()
        solution.assign(self.sortedMembers[iteration].getId()) # assign the corresponding loop member ordered by weight

        # for all members
        for iteration in range(0, self.numMembers):
            # alpha = 0 if iteration == 1 else 0.7 #self.config.alpha
            
            # compute feasible assignments
            candidateList = solution.findFeasibleAssignments()

            # If we can't add more members to the solution, break the loop
            if not candidateList:
                break
            
            # select an assignment
            alpha = 0.7
            candidate = self._selectCandidate(candidateList, alpha)

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
        
        # auxiliary variables
        self.numMembers = self.instance.getNumMembers()
        self.sortedMembers = sorted(self.instance.getMembers(), key=lambda t: t.getWeight(), reverse=True)
        self.writeLogLine(bestCompatibility, 0)

        iteration = 0
        last_time_check = time.time()
        while not self.stopCriteria():
            iteration += 1
            
            if iteration % 1000 == 0: # print elapsed time every 1000 iterations
                current_time = time.time()
                elapsed_time = current_time - last_time_check
                print(f"Elapsed time for {iteration} iterations: {elapsed_time} seconds")
                last_time_check = current_time
            
            # CONSTRUCTION FASE
            # force first iteration as a Greedy execution (alpha == 0)
            # alpha = 0 if iteration == 1 else 0.7 #self.config.alpha
            deb = False
            if deb:
                # Special case iterations debugging
                if iteration >= 100000: # max iterations
                    break
                solution = self._greedyRandomizedConstruction(random.randint(0, self.numMembers-1))
            else:
                if iteration == self.numMembers: # max iterations
                    break
                solution = self._greedyRandomizedConstruction(iteration)
            
            # LOCAL SEARCH FASE
            # TODO: implement local search
            # if self.config.localSearch:
            #     localSearch = LocalSearch(self.config, None)
            #     endTime = self.startTime + self.config.maxExecTime
            #     solution = localSearch.solve(solution=solution, startTime=self.startTime, endTime=endTime)

            # Keep the best solution found
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

