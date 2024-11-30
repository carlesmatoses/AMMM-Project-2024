import sys
import os
import parser
from generateInstance import generateInstance

def run():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    if len(sys.argv) < 2:
        config_path = os.path.join(current_dir, "config.dat")
        print("Warning: using default config file 'config.dat'")
    else:
        config_path = os.path.join(current_dir, sys.argv[1])
        print(f"reading config file: {config_path}")
        
    config = parser.parse_config(config_path)
    generateInstance(config)
    return 0

def customGenerator():
    D = [ 2,  3,  3,  3,  3,  3,  3,  3] 
    N = [10, 20, 30, 32, 34, 36, 38, 40]
    for i in range(len(D)):
        data = {
            "D": D[i],
            "N": N[i],
            "n": D[i],
            "out": f"examples/project.{D[i]}_{N[i]}.dat"
        }
        generateInstance(data)

if __name__ == '__main__':
    sys.exit(run())
    # sys.exit(customGenerator())
