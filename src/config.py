import os
from pathlib import Path

# --- PATH CONFIGURATION ---
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
SECBENCH_REPO_PATH = RAW_DIR / "SecBench.js"
TASK_FILE = DATA_DIR / "secbench.json"
SOURCE_PATH = Path("data/raw/SecBench.js")
OUTPUT_FILE = Path("data/secbench.json")

# --- PARAMETER CONFIGURATION ---
MAX_THREADS = int(os.getenv("MAX_THREADS", 4))

CATEGORIES = [
    "prototype-pollution", "redos", "command-injection", 
    "path-traversal", "ace-breakout"
]

# Use IGNORED instead of ALLOWED to support all languages
IGNORED_EXTENSIONS = (
    '.md', '.txt', '.json', '.pdf', '.jpg', '.png', '.gif', 
    '.svg', '.css', '.scss', '.lock', '.yaml', '.yml', '.csv'
)

BLOCKED_DIRS = {
    '.git', 'node_modules', 'test', 'tests', 'coverage', 
    'dist', 'docs', 'benchmark', 'examples', '.github'
}

# Mapping for Tree-sitter 
LANG_MAPPING = {
    "js": "javascript", "jsx": "javascript", "mjs": "javascript",
    "ts": "typescript", "tsx": "typescript",
    "py": "python", "java": "java", "cpp": "cpp", "c": "c"
}