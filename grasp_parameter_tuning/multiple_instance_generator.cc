#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <numeric>
#include <chrono>
#include <iomanip>
#include <fstream>

using namespace std;

int main(int argc, const char * argv[]) {
    // Check if we have the correct number of arguments
    if (argc != 5) {
        cout << "Usage: <program_name> <Number of instances to generate> <Number of departments> <Number of members in the Faculty> <Commission size>" << endl;
        return -1;
    }
    
    // Convert command-line arguments to integers
    int numInstances = stoi(argv[1]);  // Convert argv[1] to integer for I
    int D = stoi(argv[2]);  // Convert argv[2] to integer for D
    int N = stoi(argv[3]);  // Convert argv[3] to integer for N
    int commissionSize = stoi(argv[4]);  // Convert argv[4] to integer for N
    
    if (D < 1) {
        cout << "There must be at least one department" << endl;
        return -1;
    }
    if (N < 1) {
        cout << "There must be at least one member in the Faculty" << endl;
        return -1;
    }
    if (commissionSize < D) {
        cout << "The commission must have one member of each department" << endl;
        return -1;
    }
    if (commissionSize >= N) {
        cout << "The commission size cannot exceed the number of members in the Faculty" << endl;
        return -1;
    }
    
    srand(time(0));
    srand(rand()); // Ensure the seed is sufficiently different
    
    for (int instanceIndex = 1; instanceIndex <= numInstances; ++instanceIndex) {
        
        // Initialize vectors for n (size D) and d (size N)
        vector<int> n(D, 1);
        vector<int> d(N);
        vector<vector<double>> m(N, vector<double>(N));
        
        for (int p = D; p < commissionSize; ++p) {
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
        
        string filename = "input/input_instance_" + to_string(instanceIndex) + ".txt";
        ofstream file(filename);
        
        file << D << endl;
        for (int p = 0; p < D; ++p) file << n[p] << ' ';
        file << endl;
        
        file << N << endl;
        for (int i = 0; i < N; ++i) file << d[i] + 1 << ' ';
        file << endl;
        
        file << fixed << setprecision(2);  // Set fixed-point notation and 2 decimal places
        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < N; ++j) {
                file << m[i][j] << ' ';
            }
            file << endl;
        }
        file << endl;
        
    }
    
    cout << "Generated " << numInstances << " instances in the 'input' folder." << endl;
    
    return 0;
}
