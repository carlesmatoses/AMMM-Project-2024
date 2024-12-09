# This script is used to compare
# 1. greedy to CPLEX
# 2. greedy + localsearch
# 3. GRASP

import pickle
from matplotlib import pyplot as plt
plt.style.use('ggplot')

# Path to the pickle file
file_path = 'graphs/results.pkl'
file_path_greedy = 'graphs/greedy_results.pkl'
file_path_greedyLocal = 'graphs/greedyLocal_results.pkl'
file_path_grasp = 'graphs/grasp_results.pkl'

# Open the pickle file
with open(file_path, 'rb') as file:
    dataCPLEX = pickle.load(file)
with open(file_path_greedy, 'rb') as file:
    dataGreedy = pickle.load(file)
with open(file_path_greedyLocal, 'rb') as file:
    dataGreedyLocal = pickle.load(file)
with open(file_path_grasp, 'rb') as file:
    dataGrasp = pickle.load(file) 
####################
# 1. greedy to CPLEX
# Filter data for p == 1 and departments == 2
_p = 5
_d = 2
filtered_data = [d for d in dataCPLEX if d['p'] == _p and d['departments'] == _d]
filtered_data_greedy = [d for d in dataGreedy if d['p'] == _p and d['departments'] == _d]
filtered_data_greedyLocal = [d for d in dataGreedyLocal if d['p'] == _p and d['departments'] == _d]
filtered_data_grasp = [d for d in dataGrasp if d['p'] == _p and d['departments'] == _d]
   

# Order filtered data by the N value
filtered_data.sort(key=lambda x: x['members'])
filtered_data_greedy.sort(key=lambda x: x['members'])
filtered_data_greedyLocal.sort(key=lambda x: x['members'])
filtered_data_grasp.sort(key=lambda x: x['members'])

# Extract N and time values
N_values = [d['members'] for d in filtered_data]
time_values = [d['OBJECTIVE'] for d in filtered_data]
plt.plot(N_values, time_values, marker='o', label=f'Cplex Objective')

# Extract N and time values
N_values = [d['members'] for d in filtered_data_greedy]
time_values = [d['OBJECTIVE'] for d in filtered_data_greedy]
plt.plot(N_values, time_values, marker='.', label=f'Greedy Objective')

# Extract N and time values
N_values = [d['members'] for d in filtered_data_greedyLocal]
time_values = [d['OBJECTIVE'] for d in filtered_data_greedyLocal]
plt.plot(N_values, time_values, marker='.', label=f'Greedy+Local Objective')

# Extract N and time values
N_values = [d['members'] for d in filtered_data_grasp]
time_values = [d['OBJECTIVE'] for d in filtered_data_grasp]
plt.plot(N_values, time_values, marker='.', label=f'GRASP Objective')

plt.legend()
plt.xlabel('N')
plt.ylabel('Objective')
plt.title(f'Objective for committee size {_d*_p}')
plt.grid(True)
plt.show()

# 1. greedy to CPLEX
####################

with open("graphs/grasp_nolocal_results.pkl", 'rb') as file:
    dataGraspNoLocal = pickle.load(file) 

filtered_data_grasp         = [d for d in dataGrasp if d['p'] == 5 and d['departments'] == 2]
filtered_data_grasp_nolocal = [d for d in dataGraspNoLocal if d['p'] == 5 and d['departments'] == 2]

filtered_data_grasp.sort(key=lambda x: x['members'])
filtered_data_grasp_nolocal.sort(key=lambda x: x['members'])

N_values = [d['members'] for d in filtered_data_grasp]
time_values = [d['OBJECTIVE'] for d in filtered_data_grasp]
plt.plot(N_values, time_values, marker='o', label=f'GRASP with local search')

N_values = [d['members'] for d in filtered_data_grasp_nolocal]
time_values = [d['OBJECTIVE'] for d in filtered_data_grasp_nolocal]
plt.plot(N_values, time_values, marker='o', label=f'GRASP without local search')

plt.legend()
plt.xlabel('N')
plt.ylabel('Objective')
plt.title(f'Objective for GRASP with and without local search')
plt.grid(True)
plt.show()


filtered_data_grasp         = [d for d in dataGrasp if d['p'] == 5 and d['departments'] == 2]
filtered_data_grasp_nolocal = [d for d in dataGraspNoLocal if d['p'] == 5 and d['departments'] == 2]

filtered_data_grasp.sort(key=lambda x: x['members'])
filtered_data_grasp_nolocal.sort(key=lambda x: x['members'])

N_values = [d['members'] for d in filtered_data_grasp]
time_values = [d['time'] for d in filtered_data_grasp]
plt.plot(N_values, time_values, marker='o', label=f'GRASP with local search')

N_values = [d['members'] for d in filtered_data_grasp_nolocal]
time_values = [d['time'] for d in filtered_data_grasp_nolocal]
plt.plot(N_values, time_values, marker='o', label=f'GRASP without local search')

plt.legend()
plt.xlabel('N')
plt.ylabel('Time')
plt.title(f'Time for GRASP with and without local search')
plt.grid(True)
plt.show()



# grasp amb first improvement vs sense first improvement.
# velocitats de grasp first improvement vs sense first improvement.