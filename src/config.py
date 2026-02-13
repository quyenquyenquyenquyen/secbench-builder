import os
from pathlib import Path

# Define project base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Data path configuration
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"          # Directory for cloned repos
PROCESSED_DIR = DATA_DIR / "processed" # Directory for processed code
INPUT_FILE = DATA_DIR / "secbench.json"

# Number of parallel threads
MAX_THREADS = 4 

# File extension mapping (SecBench is mostly JS)
LANG_MAPPING = {
    "js": "javascript",
    "jsx": "javascript",
    "ts": "typescript",
    "tsx": "typescript",
}