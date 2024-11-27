import os

"""Parser module for parsing configuration files."""

def parse_config(config_path):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file '{config_path}' does not exist.")

    config = {}
    with open(config_path, 'r') as file:
        for line in file:
            line = line.strip()
            line = line.split('//', 1)[0].strip()
            if line and '=' in line:
                key, value = line.split('=', 1)
                value = value.strip().strip(';')
                if value.isdigit():
                    value = int(value)
                elif value.replace('.', '', 1).isdigit() and value.count('.') < 2:
                    value = float(value)
                elif value.lower() in ['true', 'false']:
                    value = value.lower() == 'true'
                config[key.strip()] = value
            elif line and '=' not in line:
                raise ValueError(f"Invalid syntax in config file at line: '{line}'")
    return config