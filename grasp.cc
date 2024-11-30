#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <numeric>
#include <cstdlib>
#include <chrono>

using namespace std;

const int MAX_ITER = 100;
const double ALPHA = 0.3;

const string SEARCH_POLICY = "FirstImprovement";

int D, N;
vector<int> n, d;
vector<vector<double>> m;

double compute_average_compatibility(const vector<bool>& commission) {
    double total_compatibility = 0.0;
    int count = 0;

    for (int i = 0; i < N; ++i) {
        if (commission[i]) {
            for (int j = i + 1; j < N; ++j) {
                if (commission[j]) {
                    total_compatibility += m[i][j];
                    count++;
                }
            }
        }
    }

    return (count == 0 ? 0.0 : total_compatibility / count);
}

bool is_valid_candidate(int candidate, const vector<bool>& commission) {
    int department = d[candidate];
    int department_count = 0;
    for (int i = 0; i < N; ++i) {
        if (commission[i] and d[i] == department) ++department_count;
    }
    if (department_count >= n[department]) return false;

    for (int i = 0; i < N; ++i) {
        if (commission[i] and m[candidate][i] == 0) return false;
        if (commission[i] and m[candidate][i] < 0.15) {
            bool intermediate = false;
            for (int j = 0; j < N; ++j) {
                if (commission[j] and m[candidate][j] > 0.85 and m[i][j] > 0.85) {
                    intermediate = true;
                    break;
                }
            }
            if (not intermediate) return false;
        }
    }
    return true;
}

double compute_candidate_compatibility(int candidate, const vector<bool>& commission) {
    double compatibility = 0.0;
    for (int i = 0; i < N; ++i) {
        if (commission[i]) {
            compatibility += m[candidate][i];
        }
    }
    return compatibility;
}

// Comparison function to compare two candidates based on their compatibility score
bool compare_candidates_by_compatibility(const pair<int, double>& a, const pair<int, double>& b) {
    return a.second < b.second;  // Sort in ascending order of compatibility score
}

vector<pair<int, double>> getCandidateScores(const vector<bool>& solution, vector<bool>& candidates) {
    vector<pair<int, double>> candidateList;
    for (int member = 0; member < N; ++member) {
        if (candidates[member]) {
            if (is_valid_candidate(member, solution)) {
//                cout << member << endl;
                double memberCompatibility = compute_candidate_compatibility(member, solution);
                candidateList.push_back({member, memberCompatibility});
            }
            else candidates[member] = false;
        }
    }
    return candidateList;
}

vector<bool> constructSolution() {
    vector<bool> candidates(N, true);
    vector<bool> solution(N, false);
    
    int commissionSize = accumulate(n.begin(), n.end(), 0);
    int solutionSize = 0;
    while (solutionSize < commissionSize) {
        vector<pair<int, double>> candidateScores = getCandidateScores(solution, candidates);
        // Return if no solution could be found
        if (candidateScores.size() == 0) return vector<bool>(N, false);
        sort(candidateScores.begin(), candidateScores.end(), compare_candidates_by_compatibility);
        double minScore = candidateScores[0].second;
        double maxScore = candidateScores[candidateScores.size() - 1].second;
        
//        cout << minScore << ' ' << maxScore << endl;
        
        vector<int> restrictedCandidateList;
        for (auto i : candidateScores) {
            int candidate = i.first;
            double score = i.second;
            if (score >= maxScore - ALPHA*(maxScore - minScore))
                restrictedCandidateList.push_back(candidate);
        }
        
        int RCL_size = restrictedCandidateList.size();
//        cout << "RCL size: " << RCL_size << endl;
        int selectedCandidate = restrictedCandidateList[rand()%RCL_size];
//        cout << "Selected candidate = " << selectedCandidate << endl;
        solution[selectedCandidate] = true;
        candidates[selectedCandidate] = false;
        ++solutionSize;
    }
    
    return solution;
}

void exploreExchange(const vector<bool>& current_solution, double& current_best_comp, vector<bool>& bestNeighbor, double& best_comp) {
    best_comp = current_best_comp;
    bestNeighbor = current_solution;
    
    for (int i = 0; i < N; ++i) {
        if (current_solution[i]) {
            vector<bool> neighbor = current_solution;
            neighbor[i] = false;  // Remove member i from the commission
            
            for (int j = 0; j < N; ++j) {
                if (not current_solution[j] and is_valid_candidate(j, neighbor)) {
                    neighbor[j] = true;  // Add candidate j to the commission
                    double comp = compute_average_compatibility(neighbor);
                    if (comp > best_comp) {
                        bestNeighbor = neighbor;
                        best_comp = comp;
                        if (SEARCH_POLICY == "FirstImprovement") return;
                    }
                    neighbor[j] = false;  // Undo the change for next candidate
                }
            }
            neighbor[i] = true;  // Re-add member i
        }
    }
}

void exploreNeighborhood(const vector<bool>& current_solution, double& current_best_comp, vector<bool>& bestNeighbor, double& best_comp) {
    exploreExchange(current_solution, current_best_comp, bestNeighbor, best_comp);
}

double local_search(vector<bool>& solution) {
    double comp = compute_average_compatibility(solution);
    while (true) {
        vector<bool> neighbor;
        double neighbor_comp;
        exploreNeighborhood(solution, comp, neighbor, neighbor_comp);
        if (neighbor_comp <= comp) return comp;  // No improvement, return the best compatibility
        comp = neighbor_comp;
        solution = neighbor;
    }
}

vector<bool> solveGrasp() {
    vector<bool> bestSolution(N, false);
    double bestCompatibility = 0;
    
    for (int k = 0; k < MAX_ITER; ++k) {
        vector<bool> solution = constructSolution();
        double compatibility = local_search(solution);
        
        if (compatibility > bestCompatibility) {
            bestSolution = solution;
            bestCompatibility = compatibility;
        }
    }
    
    cout << "Average compatibility: " << bestCompatibility << endl;
    cout << "COMMISSION: ";
    bool first = true;
    for (int i = 0; i < N; ++i) {
        if (bestSolution[i]) {
            if (not first) cout << ", ";
            cout << i + 1;
            first = false;
        }
    }
    cout << endl;
    return bestSolution;
}

int main() {
    
    srand(time(0));
    
    while (cin >> D) {
        n = vector<int>(D);
        for (int p = 0; p < D; ++p) cin >> n[p];
        
        cin >> N;
        d = vector<int>(N);
        for (int i = 0; i < N; ++i) {
            int dept;
            cin >> dept;
            d[i] = dept - 1;
        }
        
        m = vector<vector<double>>(N, vector<double>(N));
        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < N; ++j) {
                cin >> m[i][j];
            }
        }
        
        auto start = chrono::high_resolution_clock::now();  // Start timer
        solveGrasp();
        auto end = chrono::high_resolution_clock::now();    // End timer
        chrono::duration<double> elapsed = end - start;     // Elapsed time
        
        cout << "Time taken: " << elapsed.count() << " seconds." << endl;
    }
}
