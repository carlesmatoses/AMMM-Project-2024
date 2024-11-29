#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <numeric>

using namespace std;

int D, N;
vector<int> n, d;
vector<vector<double>> m;

vector<bool> candidates;


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

double compute_total_compatibility(const vector<bool>& commission) {
    double total_compatibility = 0.0;

    for (int i = 0; i < N; ++i) {
        if (commission[i]) {
            for (int j = i + 1; j < N; ++j) {
                if (commission[j]) {
                    total_compatibility += m[i][j];
                }
            }
        }
    }

    return total_compatibility;
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
    return a.second > b.second;  // Sort in descending order of compatibility score
}

int select_best_candidate(const vector<bool>& commission) {
    vector<pair<int, double>> candidate_scores;

    // Collect candidates and their compatibility scores
    for (int candidate = 0; candidate < N; ++candidate) {
        if (candidates[candidate] and is_valid_candidate(candidate, commission)) {
            double compatibility = compute_candidate_compatibility(candidate, commission);
            candidate_scores.push_back({candidate, compatibility});
        }
        else candidates[candidate] = false;
    }

    // If there are no valid candidates, return -1
    if (candidate_scores.empty()) return -1;

    // Sort the candidates by compatibility in descending order using the comparison function
    sort(candidate_scores.begin(), candidate_scores.end(), compare_candidates_by_compatibility);

    // Return the candidate with the highest compatibility score
    return candidate_scores[0].first;
}

void solve_greedy() {
    candidates = vector<bool>(N, true);  // All members are initially candidates
    vector<bool> commission = vector<bool>(N, false); // No members are in the commission initially
    
    int total_members_needed = accumulate(n.begin(), n.end(), 0);

    while (accumulate(commission.begin(), commission.end(), 0) < total_members_needed) {
        int selected_candidate = select_best_candidate(commission);
        if (selected_candidate == -1) {
            cout << "No valid solution found" << endl;
            break;
        }
        commission[selected_candidate] = true;
        candidates[selected_candidate] = false;
    }

    // Output the commission and average compatibility
    if (accumulate(commission.begin(), commission.end(), 0) == total_members_needed) {
        cout << "Commission: {";
        bool first = true;
        for (int i = 0; i < N; ++i) {
            if (commission[i]) {
                if (not first) cout << ", ";
                cout << i + 1;
                first = false;
            }
        }
        cout << "}" << endl;

        double total_compatibility = compute_total_compatibility(commission);
        int num_pairs = (total_members_needed * (total_members_needed - 1)) / 2;
        double average_compatibility = total_compatibility / num_pairs;

        cout << "Average compatibility: " << average_compatibility << endl;
    }
}

int main() {
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
        
        solve_greedy();
    }
}
