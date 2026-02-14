import json
import os
import sys
sys.setrecursionlimit(10000)
from concurrent.futures import ThreadPoolExecutor
from src.config import MAX_THREADS, TASK_FILE 
from src.preprocess.patch_parser import process_cve_task

def main():
    if not os.path.exists(TASK_FILE):
        print(f"[FATAL] Data file not found: {TASK_FILE}")
        print("-> Please run command: python3 parse_data.py to generate data first!")
        return

    print(f"[INFO] Loading data from {TASK_FILE}...")
    
    try:
        with open(TASK_FILE, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
    except json.JSONDecodeError:
        print(f"[ERROR] File {TASK_FILE} is malformed or empty.")
        return

    if not tasks:
        print("[WARN] CVE list is empty. Please check parse_data.py.")
        return

    print(f"[INFO] Processing {len(tasks)} CVEs with {MAX_THREADS} threads...")

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        results = executor.map(process_cve_task, tasks)
        
        # for res in results: print(res) 

    print(f"\n[SUCCESS] Check 'data/processed' directory for results!")

if __name__ == "__main__":
    main()