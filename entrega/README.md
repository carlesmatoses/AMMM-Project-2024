# Course Project

This project is designed to generate multiple instances of a commission assignment problem and solve it using different strategies like **Greedy**, **Greedy with Local Search**, **GRASP**, and **CPLEX** optimization.

The project consists of two main parts:

1. **Instance Generator**: Generates multiple instances of the problem with random parameters.
2. **Solver**: Solves the generated problem instances using different algorithms (Greedy, Greedy with Local Search, GRASP) or via **CPLEX** optimization.

## Features

- **Instance Generator**: Randomly generates problem instances based on configurable parameters.
- **Solvers**: 
  - **Greedy Algorithm**: Solves the problem using a simple greedy approach.
  - **Greedy with Local Search**: Enhances the greedy solution using a local search technique.
  - **GRASP Algorithm**: Uses a Greedy Randomized Adaptive Search Procedure (GRASP) for solving the problem.
  - **CPLEX Optimization**: Solves the problem using IBM ILOG CPLEX with a custom model.

## Requirements

- **C++ Compiler** (e.g., `g++` supporting C++11)
- **Make** (for building the project)
- **IBM ILOG CPLEX**: Required for solving using CPLEX.
  
Ensure that you have the necessary permissions to execute the files and write to the directories.

## Project Structure

```
/project
├── Makefile                        # Build configuration
├── project.cc                      # Solver source code
├── multiple_instance_generator.cc  # Instance generator source code
├── cpp_input/                      # Directory for the generated input files
├── cplex_input/                    # Directory for CPLEX input files
└── README.md                       # Project documentation
```


### Description of Files:

- **project.cc**: Contains the implementation of the algorithms used to solve the commission assignment problem (Greedy, Greedy with Local Search, GRASP).
- **multiple_instance_generator.cc**: Generates multiple instances of the problem based on the configuration parameters.
- **cpp_input/**: Directory where input files in `.txt` format are saved for the C++ solver.
- **cplex_input/**: Directory where input files in `.dat` format are saved for the CPLEX solver.
- **project.mod**: Defines the optimization model for solving the problem using CPLEX.
- **main.mod**: Main script to configure and run the CPLEX model.

## Compilation and Build

You can compile the project using the `Makefile`. It will build two executables: `project` (the solver) and `multiple_instance_generator` (the instance generator).

### To compile the project:

1. Clone or download the project files.
2. Open a terminal in the project directory.
3. Run the following command to build the executables:

   ```bash
   make
   ```
### To clean the build

If you want to clean the object files and executables, run:

```bash
make clean
```

### Usage

#### 1. Generate Instances
You can generate problem instances using the `multiple_instance_generator` executable. It will create multiple problem instances based on the configuration.

To run the instance generator:

```bash
./multiple_instance_generator
```

This will generate multiple problem instances and save them in the `cpp_input/` and `cplex_input/` directories in two formats:
- `cpp_input/input_instance_<index>.txt`
- `cplex_input/input_instance_<index>.dat`

Each instance contains:
- The number of departments (D)
- The number of faculty members (N)
- Department assignments for each faculty member
- Compatibility matrix (m)

#### 2. Solve Problem Instances
Once you have the instances generated, you can solve them using the project executable or via CPLEX.

**Using the C++ Solver**

To run the solver:

```bash
./project < input_instance.txt
```
This will:
- Read the problem instance from the _input_instance_ file provided.
- Solve the problem using the three different solving strategies:
  - **Greedy**
  - **Greedy with Local Search**
  - **GRASP**
- Output the results, including the average compatibility and the selected commission members.

### Configuration Parameters

In `multiple_instance_generator.cc`, the following parameters control the generation of the problem instances:
- `numInstances`: The number of instances to generate.
- `D_min`, `D_max`: The minimum and maximum number of departments.
- `N_min`, `N_max`: The minimum and maximum number of faculty members.
- `commissionSize_min`, `commissionSize_max`: The range for the commission size.

These values are defined at the beginning of `multiple_instance_generator.cc`. Adjust them as needed for different problem instance characteristics.

### Solvers

#### 1. Greedy Algorithm
The Greedy algorithm selects faculty members for the commission based on their compatibility. It iteratively adds the best candidate until the commission is full.

#### 2. Greedy with Local Search
This method first runs the Greedy algorithm, then improves the solution by applying a local search. It looks for neighboring solutions that provide a better compatibility score and iterates until no improvements can be made.

#### 3. GRASP Algorithm
GRASP (Greedy Randomized Adaptive Search Procedure) is a metaheuristic that combines a greedy solution with randomization. It explores the solution space by selecting candidates from a restricted candidate list (RCL) and improving the solution using local search. The process is repeated multiple times, and the best solution found is returned.

#### 4. CPLEX Optimization
Uses IBM ILOG CPLEX for solving the problem with the model defined in project.mod and managed by main.mod. The CPLEX model optimizes the commission assignment problem based on the provided input data.

### Example Output

Here is an example of the output you may see when running the project solver:

```
GREEDY RESULTS:
Average compatibility: 0.75
GREEDY COMMISSION: 1, 2, 5, 7, 8
Time taken: 0.34 seconds.

GREEDY WITH LOCAL SEARCH RESULTS:
Average compatibility: 0.80
GREEDY WITH LOCAL SEARCH COMMISSION: 1, 3, 5, 7, 9
Time taken: 0.56 seconds.

GRASP RESULTS:
Average compatibility: 0.85
GRASP COMMISSION: 1, 2, 4, 6, 10
Time taken to find the best solution: 2.34 seconds.
Total time taken: 3.12 seconds.
```
