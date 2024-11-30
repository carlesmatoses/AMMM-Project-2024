#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <numeric>
#include <queue>

using namespace std;

// Local Search
const string SEARCH_POLICY = "FirstImprovement";

// GRASP Constans
const int MAX_ITER = 1000;
const double ALPHA = 0.3;

int D, N;
vector<int> n, d;
vector<vector<double>> m;

/*  -----------------------------------  Input  ------------------------------------------  */

void read_input() {
    cin >> D;
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
}

/* ------------------------------ Functions for solvers ------------------------------------ */

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

bool existsIntermediate(int i, int j, const vector<bool>& commission) {
    for (int k = 0; k < N; ++k) {
        if (commission[k] and m[i][k] > 0.85 and m[j][k] > 0.85) {
            return true;
        }
    }
    return false;
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
            if (not existsIntermediate(candidate, i, commission)) return false;
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

double compute_candidate_score(int candidate, const vector<bool>& commission) {
    double score = 0.0;
    vector<int> dep_counts = n;
    --dep_counts[d[candidate]];
    priority_queue<pair<double, int>> q;
    for (int i = 0; i < N; ++i) {
        double compatibility_i = m[candidate][i];
        if (compatibility_i > 0.85) compatibility_i *= 4;
        else if (compatibility_i >= 0.15 or existsIntermediate(candidate, i, commission)) {
            compatibility_i *= 2;
        }
        else if (compatibility_i == 0) compatibility_i = -1;
        if (commission[i]) {
            score += compatibility_i;
            --dep_counts[d[i]];
        }
        else q.push({compatibility_i, i});
    }
    
    while (not q.empty()) {
        auto x = q.top(); q.pop();
        double member_compatibility = x.first;
        int member = x.second;
        if (dep_counts[d[member]] > 0) {
            score += member_compatibility;
            --dep_counts[d[member]];
        }
        else if (member_compatibility == -1) score += 0.5*member_compatibility;
    }
    
    return score;
}

bool compare_candidates_by_compatibility(const pair<int, double>& a, const pair<int, double>& b) {
    return a.second < b.second;
}

vector<pair<int, double>> getCandidateScores(const vector<bool>& solution, vector<bool>& candidates) {
    vector<pair<int, double>> candidateList;
    for (int member = 0; member < N; ++member) {
        if (candidates[member]) {
            if (is_valid_candidate(member, solution)) {
                double memberScore = compute_candidate_score(member, solution);
                candidateList.push_back({member, memberScore});
            }
            else candidates[member] = false;
        }
    }
    return candidateList;
}

vector<bool> solveGreedy() {
    vector<bool> candidates(N, true);
    vector<bool> solution(N, false);
    
    int commissionSize = accumulate(n.begin(), n.end(), 0);
    int solutionSize = 0;
    
    while (solutionSize < commissionSize) {
        vector<pair<int, double>> candidateScores = getCandidateScores(solution, candidates);
        
        // Return if no solution could be found
        if (candidateScores.size() == 0) return vector<bool>(N, false);
        
        sort(candidateScores.begin(), candidateScores.end(), compare_candidates_by_compatibility);
        int selectedCandidate = candidateScores[candidateScores.size() - 1].first;
        
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

vector<bool> constructGraspSolution() {
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
        
        vector<int> restrictedCandidateList;
        for (auto i : candidateScores) {
            int candidate = i.first;
            double score = i.second;
            if (score >= maxScore - ALPHA*(maxScore - minScore))
                restrictedCandidateList.push_back(candidate);
        }
        
        int RCL_size = restrictedCandidateList.size();
        int selectedCandidate = restrictedCandidateList[rand()%RCL_size];
        solution[selectedCandidate] = true;
        candidates[selectedCandidate] = false;
        ++solutionSize;
    }
    
    return solution;
}

/*  ---------------------------  Solving with different solving strategies  ---------------------------------  */

void solve_with_greedy() {
    auto start = chrono::high_resolution_clock::now();  // Start timer
    vector<bool> solution = solveGreedy();
    double compatibility = compute_average_compatibility(solution);
    auto end = chrono::high_resolution_clock::now();    // End timer
    chrono::duration<double> elapsed = end - start;     // Elapsed time
    
    cout << "GREEDY RESULTS:" << endl;
    cout << "Average compatibility: " << compatibility << endl;
    cout << "COMMISSION: ";
    bool first = true;
    for (int i = 0; i < N; ++i) {
        if (solution[i]) {
            if (not first) cout << ", ";
            cout << i + 1;
            first = false;
        }
    }
    cout << endl;
    
    cout << "Time taken: " << elapsed.count() << " seconds." << endl;
}

void solve_with_greedy_and_local_search() {
    auto start = chrono::high_resolution_clock::now();  // Start timer
    vector<bool> solution = solveGreedy();
    double compatibility = local_search(solution);
    auto end = chrono::high_resolution_clock::now();    // End timer
    chrono::duration<double> elapsed = end - start;     // Elapsed time
    
    cout << "GREEDY WITH LOCAL SEARCH RESULTS:" << endl;
    cout << "Average compatibility: " << compatibility << endl;
    cout << "COMMISSION: ";
    bool first = true;
    for (int i = 0; i < N; ++i) {
        if (solution[i]) {
            if (not first) cout << ", ";
            cout << i + 1;
            first = false;
        }
    }
    cout << endl;
    
    cout << "Time taken: " << elapsed.count() << " seconds." << endl;
}

void solve_with_grasp() {
    auto start = chrono::high_resolution_clock::now();  // Start timer
    
    vector<bool> bestSolution(N, false);
    double bestCompatibility = 0;
    
    for (int k = 0; k < MAX_ITER; ++k) {
        vector<bool> solution = constructGraspSolution();
        double compatibility = local_search(solution);
        
        if (compatibility > bestCompatibility) {
            bestSolution = solution;
            bestCompatibility = compatibility;
        }
    }
    
    auto end = chrono::high_resolution_clock::now();    // End timer
    chrono::duration<double> elapsed = end - start;     // Elapsed time
    
    cout << "GREEDY WITH LOCAL SEARCH RESULTS:" << endl;
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
    
    cout << "Time taken: " << elapsed.count() << " seconds." << endl;
}

int main() {
    
    read_input();
    
    solve_with_greedy();
    solve_with_greedy_and_local_search();
    solve_with_grasp();
}
