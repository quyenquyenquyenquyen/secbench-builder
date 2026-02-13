import subprocess
import json
import os

def exec_command(command, cwd=None):
    """
    Execute shell command (git clone, checkout...)
    cwd: Directory where the command will be executed
    """
    try:
        # Run command and capture output
        result = subprocess.run(
            command, 
            shell=True, 
            check=True,
            cwd=cwd,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            encoding='utf-8',
            errors='ignore' # Ignore encoding errors
        )
        return result.stdout.strip(), None
    except subprocess.CalledProcessError as e:
        return None, e.stderr.strip()

def dump_json(data, filepath):
    """Write JSON file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)