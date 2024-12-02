import subprocess
import sys
import re
import os
import time

# Check for correct number of arguments
if len(sys.argv) != 5:
    print("Usage: python run_multiple_with_best_alpha.py <num_instances> <num_departments> <num_faculty_members> <commission_size>")
    sys.exit(1)

# Parse input arguments
num_instances = int(sys.argv[1])  # Number of instances to generate
num_departments = int(sys.argv[2])  # Number of departments
num_faculty_members = int(sys.argv[3])  # Number of faculty members
commission_size = int(sys.argv[4])  # Commission size

# Output file for storing results
output_file = "results.txt"

# Folder where instances will be stored
instance_folder = "input/"
os.makedirs(instance_folder, exist_ok=True)

# Function to clear all files in the input folder
def clear_input_folder(folder):
    # Loop through all files in the folder and remove them
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    print(f"Cleared all files in the '{folder}' directory.")

# Function to display progress bar with dynamic length based on terminal width
def print_progress_bar(iteration, total, bar_length=None):
    # Get the terminal width if bar_length is not provided
    if bar_length is None:
        terminal_size = os.get_terminal_size()
        bar_length = terminal_size.columns - 20  # Set some space for text on the right
    
    percent = (iteration / total) * 100
    filled_length = int(bar_length * iteration // total)
    bar = '#' * filled_length + '.' * (bar_length - filled_length)
    print(f'\rProgress: [{bar}] {percent:.0f}%', end='', flush=True)

# Function to generate multiple instances
def generate_instances(num_instances):
    subprocess.run(["./multiple_instance_generator", str(num_instances), str(num_departments), str(num_faculty_members), str(commission_size)])

# Function to run GRASP for a specific instance and ALPHA value
def run_grasp_for_alpha(instance_file, alpha_value):
    # Run the GRASP solver with the provided instance and alpha value
    result = subprocess.run(["./solve_with_grasp", str(alpha_value)], stdin=open(instance_file, "r"), capture_output=True, text=True)
    
    # Regular expression to match the "Average compatibility" value
    match = re.search(r"Average compatibility:\s*([\d.]+)", result.stdout)
    
    if match:
        # If match is found, return the floating-point value of the compatibility
        return float(match.group(1))
    else:
        # If no match is found, return None
        return None

# Clear all existing files in the input folder before generating new instances
clear_input_folder(instance_folder)

# Generate instances
generate_instances(num_instances)

# List all generated instances
instances = [os.path.join(instance_folder, f) for f in os.listdir(instance_folder) if f.endswith(".txt")]

# ALPHA values to test
alpha_values = [i / 10.0 for i in range(11)]  # ALPHA values from 0.0 to 1.0 in steps of 0.1

# Dictionary to store best alpha and its corresponding objective value for each instance
best_alpha_per_instance = {}

progressIndex = 1
# Loop over each instance and try each ALPHA value
for instance in instances:
    best_alpha = None
    best_objective_value = -float('inf')  # Assuming we want to maximize the objective value
    
    for alpha in alpha_values:
        objective_value = run_grasp_for_alpha(instance, alpha)
        
        if objective_value is not None and objective_value > best_objective_value:
            best_alpha = alpha
            best_objective_value = objective_value
            
        # Update the progress bar after each iteration
        print_progress_bar(progressIndex, num_instances*len(alpha_values))
        progressIndex += 1
    
    # Store the best alpha and its objective value for this instance
    best_alpha_per_instance[instance] = (best_alpha, best_objective_value)
    
    

# Calculate the overall best ALPHA based on the average of all instances
total_best_value = 0
total_best_alpha = 0
valid_alpha_count = 0  # Keep track of how many valid best_alpha values we have

for instance, (best_alpha, best_objective_value) in best_alpha_per_instance.items():
    if best_alpha is not None:  # Only include valid best_alpha values
        total_best_value += best_objective_value
        total_best_alpha += best_alpha
        valid_alpha_count += 1

average_best_alpha = total_best_alpha / valid_alpha_count if valid_alpha_count > 0 else 0
average_best_value = total_best_value / valid_alpha_count if valid_alpha_count > 0 else 0

# Save results to file
with open(output_file, "w") as f:
    f.write(f"Best ALPHA values for each instance:\n")
    for instance, (best_alpha, best_objective_value) in best_alpha_per_instance.items():
        f.write(f"Instance: {instance}, Best ALPHA: {best_alpha}, Best Objective Value: {best_objective_value}\n")
    
    f.write(f"\nAverage Best ALPHA: {average_best_alpha:.2f}\n")
    f.write(f"Average Best Objective Value: {average_best_value:.2f}\n")

# Print final results
print(f"Best ALPHA values for each instance have been saved to {output_file}.")
