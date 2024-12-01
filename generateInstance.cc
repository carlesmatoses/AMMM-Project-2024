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
using namespace std;

int D = 5; 
int N = 200;
int n = 4; 

char out[] = "examples/project.dat";

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

    map<int, int> percent = {{0, 5}, {14, 5}, {1, 10}};
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<> dis(0.0, 1.0);

    for (auto& comb : combinations_dic) {
        double value = round(dis(gen) * 100.0) / 100.0;
        if (value < percent[0] / 100.0) {
            value = 0.00;
        } else if (value < percent[0] / 100.0 + percent[14] / 100.0) {
            value = 0.14;
        } else if (value > 1 - percent[1] / 100.0) {
            value = 1.00;
        }
        comb.second = round(value * 100.0) / 100.0;
    }

    for (int i = 0; i < N; ++i) {
        for (int j = i + 1; j < N; ++j) {
            matrix[i][j] = combinations_dic[make_pair(i, j)];
            matrix[j][i] = matrix[i][j];
        }
    }

    return matrix;
}

int main() {
    vector<int> n_result            = vector<int>(D, n);
    vector<int> d_result            = generate_department_for_member(D,N); 
    vector<vector<double>> m_result = generate_matrix(N);

    cout << D << endl;
    cout << " ";
    for (int i = 0; i < D; ++i) {
        cout << n_result[i] << " ";
    }
    cout << endl;

    cout << "" << endl;
    cout << N << endl;
    cout << " ";
    for (int i = 0; i < N; ++i) {
        cout << d_result[i] << " ";
    }
    cout << endl;

    cout << "" << endl;
    for (int i = 0; i < N; ++i) {
        cout << " ";
        for (int j = 0; j < N; ++j) {
            cout << fixed << setprecision(2) << m_result[i][j] << " ";
        }
        cout << endl;
    }

    return 0;
}