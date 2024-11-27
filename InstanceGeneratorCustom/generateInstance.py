# The resulting file will look like this:
# D = config["D"]; # Number of departments
# n = [...]; # Number of members in each department

import random
import json

def generate_members_for_department(D, N, constant=0):
    if constant:
        return [constant] * D
    
    max_members_per_department = N // D
    members = [random.randint(1, max_members_per_department) for _ in range(D)]
    return members

def generate_department_for_member(D, N):
    members = []
    group_size = N // D
    remainder = N % D
    for i in range(1, D + 1):
        members.extend([i] * group_size)
    members.extend([D] * remainder)
    return members

def generate_matrix(N):
    matrix = []
    for i in range(N):
        row = []
        for j in range(N):
            if i == j:
                row.append(1.00)  # Diagonal elements are 1
            else:
                value = round(random.uniform(0, 1), 2)
                if value < 0.02:
                    value = 0
                elif value < 0.04:
                    value = 0.14
                elif value < 0.85:
                    value = max((value+2)/3,0.15)
                elif value > 0.85:
                    value = 1 
                row.append(value)
        matrix.append(row)
    return matrix

def write_to_file(filename, data):
    with open(f"{filename}", 'w') as file:
        file.write(f"D = {data['D']};\n")
        file.write(f"n = {json.dumps(data['n']).replace(',', '')};\n\n")
        file.write(f"N = {data['N']};\n")
        file.write(f"d = {json.dumps(data['d']).replace(',', '')};\n")
        file.write("m = [\n")
        for row in data['m']:
            formatted_row = ' '.join(f"{num:1.2f}" for num in row)
            file.write(f"    [{formatted_row}]\n")
        file.write("];\n")
    return 0


def check_n(N,n):
    # check if sum of members per department exceeds total number of members
    n_ = 0
    for i in n:
        n_+=i
    
    if n_ > N:
        raise AssertionError("Sum of members per department exceeds total number of members")
      
def check_d(N, d):
    # d length must be equal to N
    if len(d) != N:
        raise AssertionError("Length of d must be equal to N")

def check_D_N(D,N):
    # check if D is greater than N
    if D > N:
        raise AssertionError("D must be less than or equal to N")

def check_members_aviability(d,n):
    # check if required members in each department exceed the number of members in that department
    for i in range(len(n)):
        required_members = n[i]
        members = d.count(i+1)
        if required_members > members:
            raise AssertionError(f"There are not enough members to fill the department {i+1}")
        
def generateInstance(data):
    D = data["D"]  # Number of departments
    N = data["N"]  # Total number of members
    n = data["n"]  # Number of members in each department
    out = data["out"]  # Output file
    check_D_N(D,N)
    
    required_members_per_department = generate_members_for_department(D, N, n)
    members_department = generate_department_for_member(D, N)
    
    check_n(N, required_members_per_department)
    check_d(N, members_department)
    check_members_aviability(members_department, required_members_per_department)
    
    matrix = generate_matrix(N)

    file_result = write_to_file(out, {
        "D": D,
        "N": N,
        "n": required_members_per_department,
        "d": members_department,
        "m": matrix
        }
    )   
    if file_result == 0:
        print(f"File stored successfully {out}")

if "__main__" == __name__:
    # Example usage
    D = 2  # Number of departments
    N = 8  # Total number of members
    required_members_per_department = generate_members_for_department(D, N, 0)
    print(f"n: {required_members_per_department}")
    
    members_department = generate_department_for_member(D, N)
    print(f"d: {members_department}")
    
    matrix = generate_matrix(N)
    for row in matrix:
        print(row)
    
    write_to_file("members.dat", {
        "D": D,
        "N": N,
        "n": required_members_per_department,
        "d": members_department,
        "m": matrix
        }
    )
    # Stringify the array and store it in a file
    # with open('members.txt', 'w') as file:
        # json.dump(required_members_per_department, file)