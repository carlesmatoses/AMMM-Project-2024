#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <numeric>
#include <chrono>
#include <random>
#include <map>
#include <utility>
#include <iomanip>
#include <fstream>
using namespace std;

vector<int> generate_department_for_member(int D, int N) {
    vector<int> members;
    int group_size = N / D;
    int remainder = N % D;
    for (int i = 1; i <= D; ++i) {
        members.insert(members.end(), group_size, i);
    }
    members.insert(members.end(), remainder, D);
    return members;
}

vector<vector<double>> generate_matrix(int N) {
    vector<vector<double>> matrix(N, vector<double>(N, 0.0));
    for (int i = 0; i < N; ++i) {
        matrix[i][i] = 1.0;
    }

    vector<pair<int, int>> combinations_list;
    for (int i = 0; i < N; ++i) {
        for (int j = i + 1; j < N; ++j) {
            combinations_list.push_back(make_pair(i, j));
        }
    }

    map<pair<int, int>, double> combinations_dic;
    for (const auto& comb : combinations_list) {
        combinations_dic[comb] = 0.0;
    }

    // Fill the matrix with random values for demonstration purposes
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<> dis(0.0, 1.0);
    for (const auto& comb : combinations_list) {
        double value = dis(gen);
        matrix[comb.first][comb.second] = value;
        matrix[comb.second][comb.first] = value;
    }

    return matrix;
}

void save_instance(const string& filename, int D, int N, int n, const vector<int>& departments, const vector<vector<double>>& matrix) {
    ofstream outfile(filename);
    outfile << "D = " << D << ";\n";

    outfile << "n = [ ";
    for (int i = 0; i < D; ++i) {
        outfile << n << " ";
    }
    outfile << "];\n";

    outfile << "N = " << N << ";\n";

    outfile << "d = [";
    for (int dep : departments) {
        outfile << dep << " ";
    }
    outfile << "];\n";

    outfile << "m = [\n";
    for (const auto& row : matrix) {
        outfile << "[";
        for (double val : row) {
            outfile << fixed << setprecision(2) << val << " ";
        }
        outfile << "]\n";
    }
    outfile << "];\n";

    outfile.close();
}

int main() {
    int min_value = 8;
    int max_value = 100;
    vector<int> N_values(max_value - min_value + 1);
    iota(N_values.begin(), N_values.end(), min_value);
    vector<int> D_values = {2}; // Example values
    vector<int> n_values = {1}; // Example values

    int instance_count = 0;
    for (int D : D_values) {
        for (int n : n_values) {
            for (int N : N_values) {

                if (D * n > N) {
                    continue;
                }

                vector<int> departments = generate_department_for_member(D, N);
                vector<vector<double>> matrix = generate_matrix(N);
                string filename = "instances/D-" + to_string(D) + "_n-" + to_string(n) + "_N-" + to_string(N)  + ".dat";
                save_instance(filename, D, N, n, departments, matrix);
                instance_count++;
            }
        }
    }

    return 0;
}

// 1. for D = 2 and n = 2, generate instances for N = 8, 9, 10, ..., 200