import os
import fnmatch
from pathlib import Path


def parse_gitignore(gitignore_path):
    """Parse .gitignore file and return patterns"""
    ignore_patterns = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    ignore_patterns.append(line)
    return ignore_patterns


def is_ignored(path, ignore_patterns, additional_ignores):
    """Check if a path should be ignored based on patterns"""
    relative_path = str(Path(path).relative_to(root_dir)) if path != root_dir else path

    # Always ignore these
    if any(part in {'.git', '.venv'} for part in Path(path).parts):
        return True

    # Check additional
    for pattern in additional_ignores:
        if fnmatch.fnmatch(relative_path, pattern) or relative_path == pattern:
            return True

    # Check .gitignore
    for pattern in ignore_patterns:
        if pattern.endswith('/'):
            if fnmatch.fnmatch(relative_path, pattern.rstrip('/')) or \
               fnmatch.fnmatch(relative_path, f"{pattern.rstrip('/')}/*"):
                return True
        else:
            if fnmatch.fnmatch(relative_path, pattern) or \
               fnmatch.fnmatch(os.path.basename(path), pattern):
                return True

    return False


def display_tree(path, ignore_patterns, additional_ignores, prefix=""):
    """Recursively print the directory tree"""
    if is_ignored(path, ignore_patterns, additional_ignores):
        return

    entries = []
    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        print(f"{prefix}⚠️ [Permission denied] {os.path.basename(path)}/")
        return

    entries = [e for e in entries if not is_ignored(os.path.join(path, e), ignore_patterns, additional_ignores)]
    entries_count = len(entries)

    basename = os.path.basename(path)
    if prefix == "":
        print(f"📂 {basename}/")  # Only for root


    for index, entry in enumerate(entries):
        entry_path = os.path.join(path, entry)
        is_last = index == (entries_count - 1)
        connector = '└── ' if is_last else '├── '
        sub_prefix = '    ' if is_last else '│   '

        if os.path.isdir(entry_path):
            print(f"{prefix}{connector}📂 {entry}/")
            display_tree(entry_path, ignore_patterns, additional_ignores, prefix + sub_prefix)
        else:
            print(f"{prefix}{connector}📄 {entry}")


def get_user_input():
    """Get user input with error handling"""
    try:
        user_input = input("\nEnter additional files/folders to ignore (comma separated, or press Enter to skip): ")
        return [x.strip() for x in user_input.split(',') if x.strip()]
    except KeyboardInterrupt:
        print("\nOperation cancelled. Using default ignores only.")
        return []
    except Exception as e:
        print(f"\nError: {e}. Please try again.")
        return []


# Common ignore patterns
common_ignore_files = [
    '*.pyc', '*.pyo', '*.pyd', '*.db', '*.sqlite3', '*.log',
    '*.tmp', '*.bak', '*.swp', '*.swo', '*.DS_Store', 'Thumbs.db'
]

common_ignore_folders = [
    '__pycache__', '.idea', '.vscode', 'venv', 'env', '.env',
    'node_modules', 'dist', 'build', 'target', 'bin', 'obj'
]

print("Common ignored files:", ', '.join(common_ignore_files))
print("Common ignored folders:", ', '.join(common_ignore_folders))

additional_ignores = get_user_input()
additional_ignores = additional_ignores + common_ignore_files + common_ignore_folders

# Find root dir (where .gitignore exists or stop at system root)
root_dir = os.path.abspath('.')
while True:
    gitignore_path = os.path.join(root_dir, '.gitignore')
    if os.path.exists(gitignore_path) or root_dir == os.path.dirname(root_dir):
        break
    root_dir = os.path.dirname(root_dir)

ignore_patterns = parse_gitignore(gitignore_path)

print("\nFile and Folder Structure:\n")
display_tree(root_dir, ignore_patterns, additional_ignores)
