import os
import json
import re
from pathlib import Path
# Import CATEGORIES from config
from src.config import SOURCE_PATH, OUTPUT_FILE, CATEGORIES 

def parse_github_url(url):
    if not url or "github.com" not in url: return None, None
    match = re.search(r'github\.com/([^/]+)/([^/]+).*/commits?/([a-f0-9]{40})', url)
    if match:
        return f"https://github.com/{match.group(1)}/{match.group(2)}.git", match.group(3)
    return None, None

def main():
    if not SOURCE_PATH.exists():
        print(f"[ERROR] {SOURCE_PATH} not found. Please clone SecBench.js first!")
        return

    tasks = []
    print("[*] Scanning data from SecBench.js...")

    for category in CATEGORIES:
        cat_dir = SOURCE_PATH / category
        if not cat_dir.exists(): continue
        
        for item in cat_dir.iterdir():
            if item.is_dir():
                pkg_file = item / "package.json"
                if pkg_file.exists():
                    try:
                        with open(pkg_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        fix_commit = data.get('fixCommit')
                        if fix_commit:
                            repo, commit = parse_github_url(fix_commit)
                            if repo and commit:
                                tasks.append({
                                    "cve_id": data.get('id') or item.name,
                                    "type": category,
                                    "url": repo,
                                    "commit": commit
                                })
                    except: pass

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=4)
    
    print(f"[SUCCESS] Created {OUTPUT_FILE} with {len(tasks)} tasks.")

if __name__ == "__main__":
    main()