import os
import shutil
from pathlib import Path
from src.config import RAW_DIR, PROCESSED_DIR
from src.utils import exec_command
from src.preprocess.code_parser import remove_comments  # Import comment removal function

class SecBenchRetriever:
    def __init__(self, repo_url, commit_hash, cve_id, category):
        self.repo_url = repo_url
        self.commit_hash = commit_hash
        self.cve_id = cve_id
        self.category = category
        
        # Temporary directory name for cloning
        self.repo_name = self.repo_url.split('/')[-1].replace('.git', '')
        self.clone_path = RAW_DIR / "temp_clones" / self.repo_name
        
        # Output path: data/processed/category/cve_id
        self.output_root = PROCESSED_DIR / self.category / self.cve_id
        
        # Create directories
        self.output_root.mkdir(parents=True, exist_ok=True)
        (RAW_DIR / "temp_clones").mkdir(parents=True, exist_ok=True)

    def _clone_repo(self):
        # Only clone if it doesn't exist
        if not self.clone_path.exists():
            print(f"[*] Cloning {self.repo_url}...")
            exec_command(f"git clone {self.repo_url} {str(self.clone_path)}")

    def _process_and_copy(self, src_dir, dst_dir):
        """
        Iterate through files, filter junk files, remove comments, and save to destination directory
        """
        if os.path.exists(dst_dir):
            shutil.rmtree(dst_dir)
        os.makedirs(dst_dir)
        
        # Code file extensions to keep
        allowed_ext = ('.js', '.ts', '.jsx', '.tsx', '.mjs')
        # Directories to ignore
        blocked_dirs = {'.git', 'node_modules', 'test', 'tests', 'coverage', 'dist', 'docs', 'benchmark', 'examples'}

        for root, dirs, files in os.walk(src_dir):
            # Filter out junk directories to prevent deep traversal
            dirs[:] = [d for d in dirs if d not in blocked_dirs]
            
            for file in files:
                if file.lower().endswith(allowed_ext):
                    # Ignore test/spec files even if they have .js extension
                    if 'test' in file.lower() or 'spec' in file.lower():
                        continue

                    src_file_path = Path(root) / file
                    
                    # Create corresponding path in destination
                    relative_path = src_file_path.relative_to(src_dir)
                    dst_file_path = dst_dir / relative_path
                    
                    try:
                        # 1. Read original content
                        with open(src_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            original_code = f.read()
                        
                        # 2. Remove comments (Core logic)
                        clean_code = remove_comments(original_code)
                        
                        # 3. Write to destination file
                        dst_file_path.parent.mkdir(parents=True, exist_ok=True)
                        with open(dst_file_path, 'w', encoding='utf-8') as f:
                            f.write(clean_code)
                            
                    except Exception as e:
                        print(f"[WARN] Error processing file {src_file_path}: {e}")

    def run(self):
        try:
            self._clone_repo()
            
            # 1. Process AFTER version (Fixed)
            exec_command(f"git checkout -f {self.commit_hash}", cwd=str(self.clone_path))
            self._process_and_copy(self.clone_path, self.output_root / "after")
            
            # 2. Process BEFORE version (Vulnerable) - 1 step prior commit
            parent_hash, _ = exec_command(f"git rev-parse {self.commit_hash}^", cwd=str(self.clone_path))
            if parent_hash:
                exec_command(f"git checkout -f {parent_hash.strip()}", cwd=str(self.clone_path))
                self._process_and_copy(self.clone_path, self.output_root / "before")
            
            print(f"[DONE] {self.cve_id}")
            
        except Exception as e:
            print(f"[ERR] {self.cve_id}: {e}")

# --- ADD THIS FUNCTION TO BE CALLABLE FROM MAIN.PY ---
def process_cve_task(data):
    # Get category from json, default to 'misc' if missing
    category = data.get('type', 'misc') 
    retriever = SecBenchRetriever(data['url'], data['commit'], data['cve_id'], category)
    retriever.run()
    return f"Done {data['cve_id']}"