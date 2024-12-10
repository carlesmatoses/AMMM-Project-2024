#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <numeric>
#include <chrono>
#include <iomanip>
#include <fstream>

using namespace std;

int main() {
    
    // Configuration parameters
    int numInstances = 10;
    int D_min = 2;
    int D_max = 4;
    int N_min = 10;
    int N_max = 50;
    int commissionSize_min = 5;
    int commissionSize_max = 10;
    
    // Validate the configuration parameters
    if (D_min < 1 or D_min > D_max) {
        cout << "Error: Invalid department range (D_min and D_max)." << endl;
        return -1;
    }
    if (N_min < 1 or N_min > N_max) {
        cout << "Error: Invalid faculty range (N_min and N_max)." << endl;
        return -1;
    }
    if (commissionSize_min < 1 or commissionSize_min > commissionSize_max) {
        cout << "Error: Invalid commission size range (commissionSize_min and commissionSize_max)." << endl;
        return -1;
    }
    if (commissionSize_min < D_min) {
        cout << "Error: The minimum commission size must be at least as large as the number of departments (D_min)." << endl;
        return -1;
    }
    if (commissionSize_max > N_max) {
        cout << "Error: The maximum commission size cannot exceed the number of members in the Faculty (N_max)." << endl;
        return -1;
    }
    
    srand(time(0));
    srand(rand()); // Ensure the seed is sufficiently different
    
    for (int instanceIndex = 1; instanceIndex <= numInstances; ++instanceIndex) {
        
        int D = D_min + rand() % (min(D_max, commissionSize_max) - D_min + 1);
        int N = max(N_min, commissionSize_min) + rand() % (N_max - max(N_min, commissionSize_min) + 1);
        int commissionSize = max(D, commissionSize_min) + rand() % (min(N, commissionSize_max) - max(D, commissionSize_min) + 1);
        
        // Initialize vectors for n (size D) and d (size N)
        vector<int> n(D, commissionSize/D);
        vector<int> d(N);
        vector<vector<double>> m(N, vector<double>(N));
        
        for (int k = 0; k < commissionSize%D; ++k) {
            int department = rand()%D;
            ++n[department];
        }
        
        int i = 0;
        for (int p = 0; p < D; ++p) {
            for (int k = 0; k < n[p]; ++k)
                d[i++] = p;
        }
        while (i < N) d[i++] = rand()%D;
        sort(d.begin(), d.end());
        
        for (int i = 0; i < N; ++i) {
            m[i][i] = 1;
            for (int j = i + 1; j < N; ++j) {
                m[i][j] = m[j][i] = double(rand()%21)/20;
            }
        }
        
        string cpp_filename = "cpp_input/input_instance_" + to_string(instanceIndex) + ".txt";
        ofstream cpp_input(cpp_filename);
        
        cpp_input << D << endl;
        for (int p = 0; p < D; ++p) cpp_input << n[p] << ' ';
        cpp_input << endl;
        
        cpp_input << N << endl;
        for (int i = 0; i < N; ++i) cpp_input << d[i] + 1 << ' ';
        cpp_input << endl;
        
        cpp_input << fixed << setprecision(2);  // Set fixed-point notation and 2 decimal places
        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < N; ++j) {
                cpp_input << m[i][j] << ' ';
            }
            cpp_input << endl;
        }
        cpp_input << endl;
        
        string cplex_filename = "cplex_input/input_instance_" + to_string(instanceIndex) + ".dat";
        ofstream cplex_input(cplex_filename);
        
        cplex_input << "D = " << D << ";" << endl;
        cplex_input << "n = [";
        for (int p = 0; p < D; ++p) cplex_input << " " << n[p];
        cplex_input << " ];" << endl << endl;
        
        cplex_input << "N = " << N << ";" << endl;
        cplex_input << "d = [";
        for (int i = 0; i < N; ++i) cplex_input << " " << d[i] + 1;
        cplex_input << " ];" << endl << endl;
        
        cplex_input << fixed << setprecision(2);  // Set fixed-point notation and 2 decimal places
        cplex_input << "m = [" << endl;
        for (int i = 0; i < N; ++i) {
            cplex_input << "[";
            for (int j = 0; j < N; ++j) {
                cplex_input << " " << m[i][j];
            }
            cplex_input << " ]" << endl;
        }
        cplex_input << "];" << endl;
        
    }
    
    cout << "Generated " << numInstances << " instances." << endl;
    
    return 0;
}
