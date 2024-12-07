import pickle

# Path to the pickle file
file_path = 'graphs/results.pkl'

# Open the pickle file
with open(file_path, 'rb') as file:
    data = pickle.load(file)

# format of file:
# [
#   {
#       'members': 32, 
#       'departments': 2, 
#       'p': 5, 
#       'OBJECTIVE': 0.706222222, 
#       'commission': [3, 5, 6, 7, 12, 18, 21, 26, 30, 31], 
#       'time': 3.0
#   },
# ]


# Print the loaded data
print(data)

import matplotlib.pyplot as plt
plt.style.use('ggplot')

# This script is for generating the following plots:
# 1. How much does p affect the execution time
#   for D = 2 , p = 1,2,3,4,5,  against N
# 2. How much does D affect the solution time
#   for p = 2 , D = 2,4, against N
#   for p = 3 , D = 2,4, against N
# 3. N size
#   for N = 30, commission size of 2, 4, 6, 8 
# 4. Conclusion, comission size is the main factor for time increments
    # for a commission of size 6 we have:
    # D=2 and p=4
    # D=4 and p=2
    # check if they take diferent time execution.
    
    
# PLOT 1 ########################################
_p=1
_d=2

# Filter data for p == 1 and departments == 2
filtered_data = [
        [d for d in data if d['p'] == _p and d['departments'] == _d],
        [d for d in data if d['p'] == _p+1 and d['departments'] == _d],
        [d for d in data if d['p'] == _p+2 and d['departments'] == _d],
        [d for d in data if d['p'] == _p+3 and d['departments'] == _d]
    ]
# Order filtered data by the N value
for i in range(0,4):
    filtered_data[i].sort(key=lambda x: x['members'])

    # Extract N and time values
    N_values = [d['members'] for d in filtered_data[i]]
    time_values = [d['time'] for d in filtered_data[i]]

    # Plot the data
    plt.plot(N_values, time_values, marker='o', label=f'p={_p+i}')
    

plt.legend()
plt.xlabel('N')
plt.ylabel('time')
plt.title(f'Time vs N for D=2')
plt.ylim(-0.1, 1800)
plt.grid(True)
plt.show()
# PLOT 1 ########################################
#################################################


# PLOT 2 ########################################
_p=2
_d=(2,4)

# Filter data for p == 1 and departments == 2
filtered_data = [
        [d for d in data if d['p'] == _p and d['departments'] == _d[0]],
        [d for d in data if d['p'] == _p and d['departments'] == _d[1]],
    ]
# Order filtered data by the N value
for i in range(0,2):
    filtered_data[i].sort(key=lambda x: x['members'])

    # Extract N and time values
    N_values = [d['members'] for d in filtered_data[i]]
    time_values = [d['time'] for d in filtered_data[i]]

    # Plot the data
    plt.plot(N_values, time_values, marker='o', label=f'D={_d[i]}')
    

plt.legend()
plt.xlabel('N')
plt.ylabel('time')
plt.title(f'Time vs N for p=2')
plt.ylim(-0.1, 1800)
plt.grid(True)
plt.show()
# PLOT 2 ########################################
#################################################


# PLOT 3 ########################################
_p=2
_d=(2,4)

# Filter data for p == 1 and departments == 2
filtered_data = [
        [d for d in data if d['members'] == 30 and d['departments'] ==2 and d['departments']*d['p']==2],
        [d for d in data if d['members'] == 30 and d['departments'] ==2 and d['departments']*d['p']==4],
        [d for d in data if d['members'] == 30 and d['departments'] ==2 and d['departments']*d['p']==6],
    ]
# Order filtered data by the N value
res = {}
for i in range(0,3):
    # filtered_data[i].sort(key=lambda x: x['members'])

    # Extract N and time values
    # N_values = [d['members'] for d in filtered_data[i]]
    time_values = [d['time'] for d in filtered_data[i]]
    res[(i+1)*2] = sum(time_values)/len(time_values)

    # Plot the data
    # plt.plot(N_values, time_values, marker='o', label=f'D={_d[i]}')

# Plot the data from the res dictionary
plt.bar(res.keys(), res.values(), tick_label=[str(k) for k in res.keys()])

# Add labels and title
plt.xlabel('Commission Size')
plt.ylabel('Total Time')
plt.title('Total Time vs Commission Size for N=30')
plt.grid(True)

# plt.legend()
# plt.xlabel('N')
# plt.ylabel('time')
# plt.title(f'Time vs N for p=2')
# plt.ylim(-0.1, 1800)
# plt.grid(True)
plt.show()
# PLOT 3 ########################################
#################################################

# get the data 
# D=2 and p=4 and N=30
# D=4 and p=2 and N=30

# Get the data for D=2, p=4, N=30 and D=4, p=2, N=30
result_data = [
    [d for d in data if d['departments'] == 2 and d['p'] == 4 and d['members'] == 30],
    [d for d in data if d['departments'] == 4 and d['p'] == 2 and d['members'] == 30],
    [d for d in data if d['departments'] == 2 and d['p'] == 4 and d['members'] == 54],
    [d for d in data if d['departments'] == 4 and d['p'] == 2 and d['members'] == 54],
]

# Print the results
for i, res in enumerate(result_data):
    print(f"Result {i+1}:")
    for entry in res:
        print(entry)
        
# Result 1:
# {'members': 30, 'departments': 2, 'p': 4, 'OBJECTIVE': 0.7125, 'commission': [1, 3, 9, 14, 16, 17, 20, 21], 'time': 3.47}
# Result 2:
# {'members': 30, 'departments': 4, 'p': 2, 'OBJECTIVE': 0.691428571, 'commission': [3, 7, 8, 12, 15, 18, 22, 28], 'time': 0.56}