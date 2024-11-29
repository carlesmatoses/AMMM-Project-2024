#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <numeric>

using namespace std;

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

    return total_compatibility / count;
}

bool is_valid_candidate(int candidate, const vector<bool> commission) {
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
        for (int i = 0; i < N; ++i) cout << neighbor[i] << ' ';
        cout << endl;
        if (neighbor_comp <= comp) return comp;  // No improvement, return the best compatibility
        comp = neighbor_comp;
        solution = neighbor;
    }
}

int main() {
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
    
    int commission_size = accumulate(n.begin(), n.end(), 0);
    cout << commission_size << endl;
    vector<bool> solution(N, false);
    for (int i = 0; i < commission_size; ++i) {
        int member;
        cin >> member;
        solution[member - 1] = true;
    }
    
    double comp = local_search(solution);
    
    cout << "{ ";
    for (int i = 0; i < N; ++i) {
        if (solution[i]) cout << i + 1 << ' ';
    }
    cout << '}' << endl;
    cout << "Avg comp: " << comp << endl;
    
}
