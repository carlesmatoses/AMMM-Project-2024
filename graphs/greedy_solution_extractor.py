import os
import pickle

# given a folder results/ with the results of the cplex solver, this script extracts the solutions and writes them to a file
# The files are named as: D-{D}_n-{n}_N-{N}_results.txt
# where D, n and N are the parameters of the problem
# The solutions are written in the following format:
# <<< solve


# OBJECTIVE: 4.47
# OBJECTIVE: 0.745
# Commission: 1 2 7 8

# <<< post process


# <<< done

# Write a function that iterates over all files in results/ folder.
# For each file, extract the second OBJECTIVE value and the commission array
folder = "results_grasp_noLocalSearch"
output = "grasp_nolocal_results"
comp_string = "Average compatibility:"
time_string = "Time taken:"
commission_string = "GRASP COMMISSION:"

def extract_sol(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        objective = None
        commission = None
        time = None
        for line in lines:
            if line.startswith(comp_string):
                objective = line.split(":")[1].strip()
                objective = float(objective)
            elif line.startswith(commission_string):
                commission_str = line.split(":")[1].strip()
                if commission_str == "Commission not found":
                    commission = None
                else:
                    commission = commission_str.split(", ")
                    commission = [int(x) for x in commission]
            elif line.startswith(time_string):
                time = line.split(":")[1].strip().split(" ")[0]
                time = float(time)
    return objective, commission, time

def extract_variables(file_name):
    # extract D N and n from the file name
    D = N = n = 0
    for part in file_name.split("_"):
        if part.startswith("D-"):
            D = int(part.split("-")[1])
        elif part.startswith("N-"):
            N = int(part.split("-")[1])
        elif part.startswith("n-"):
            n = int(part.split("-")[1])
    return D, N, n

def solution_object(N,D,n,time,Objective,commission):
    sol = {
        "members": N, 
        "departments": D,
        "p": n,
        "OBJECTIVE": Objective, 
        "commission": commission, 
        "time": time, 
    }
    return sol

if __name__ == "__main__":



    path = os.getcwd()
    files = os.listdir(f"{path}/{folder}")
    invalid_files = []
    
    results = []
    
    for file in files:
        print(file)
        # get variables
        D, N, n = extract_variables(file)
        print(f"{D}, {N}, {n}")
        # get solution
        objective, commission, time = extract_sol(f"{path}/{folder}/{file}")
        print(f"OBJECTIVE: {objective}")
        print(f"Commission: {commission}")
        print(f"Time: {time}")
        
        if time is None or objective is None or commission is None:
            invalid_files.append(file)
        else:
            # add the solution_object on the results list
            results.append(solution_object(N,D,n,time,objective,commission))
            
    with open(f"graphs/{output}.pkl", "wb") as f:
        pickle.dump(results, f)
        
        
    print(invalid_files)

        
