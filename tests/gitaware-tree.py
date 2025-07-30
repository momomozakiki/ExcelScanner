import os
import fnmatch
from pathlib import Path

# Default patterns used only to generate a new .gitignore if missing
DEFAULT_IGNORE_FILES = [
    '*.pyc', '*.pyo', '*.pyd', '*.db', '*.sqlite3', '*.log',
    '*.tmp', '*.bak', '*.swp', '*.swo', '*.DS_Store', 'Thumbs.db'
]
DEFAULT_IGNORE_FOLDERS = [
    '__pycache__', '.idea', '.vscode', 'venv', 'env', '.env',
    'node_modules', 'dist', 'build', 'target', 'bin', 'obj'
]


def find_project_root():
    """Find the project root directory where .gitignore exists or stop at system root"""
    root = os.path.abspath('.')
    while True:
        if os.path.exists(os.path.join(root, '.gitignore')) or root == os.path.dirname(root):
            return root
        root = os.path.dirname(root)


def ensure_gitignore_exists(gitignore_path):
    """Create .gitignore if it doesn't exist"""
    if not os.path.exists(gitignore_path):
        print(f"🆕 Creating .gitignore at: {gitignore_path}")
        with open(gitignore_path, 'w') as f:
            for item in DEFAULT_IGNORE_FILES + [d + '/' for d in DEFAULT_IGNORE_FOLDERS]:
                f.write(item + '\n')


def parse_gitignore(gitignore_path):
    """Read .gitignore and return patterns"""
    patterns = []
    with open(gitignore_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                patterns.append(line)
    return patterns


def show_gitignore(gitignore_path):
    """Print all current patterns in .gitignore"""
    print("\n📄 Current .gitignore patterns:")
    with open(gitignore_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                print("  -", line)


def add_gitignore(gitignore_path, pattern):
    """Add a new pattern to .gitignore if not already present"""
    patterns = parse_gitignore(gitignore_path)
    if pattern not in patterns:
        with open(gitignore_path, 'a') as f:
            f.write(pattern + '\n')
        print(f"✅ Added '{pattern}' to .gitignore")
    else:
        print(f"ℹ️ Pattern '{pattern}' already exists in .gitignore")


def remove_gitignore(gitignore_path, pattern):
    """Remove a pattern from .gitignore if present"""
    lines_removed = 0
    with open(gitignore_path, 'r') as f:
        lines = f.readlines()

    with open(gitignore_path, 'w') as f:
        for line in lines:
            if line.strip() != pattern:
                f.write(line)
            else:
                lines_removed += 1

    if lines_removed:
        print(f"🗑️ Removed '{pattern}' from .gitignore")
    else:
        print(f"⚠️ Pattern '{pattern}' not found in .gitignore")


def is_ignored(path, ignore_patterns, root_dir):
    """Check if a path is ignored by .gitignore"""
    rel_path = str(Path(path).relative_to(root_dir)) if path != root_dir else path

    if any(part in {'.git', '.venv'} for part in Path(path).parts):
        return True

    for pattern in ignore_patterns:
        if pattern.endswith('/'):
            pattern = pattern.rstrip('/')
            if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(rel_path, f"{pattern}/*"):
                return True
        else:
            if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
                return True

    return False


def display_tree(path, ignore_patterns, root_dir, prefix=""):
    """Display directory tree respecting .gitignore"""
    if is_ignored(path, ignore_patterns, root_dir):
        return

    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        print(f"{prefix}⚠️ [Permission denied] {os.path.basename(path)}/")
        return

    entries = [e for e in entries if not is_ignored(os.path.join(path, e), ignore_patterns, root_dir)]
    total = len(entries)

    if prefix == "":
        print(f"📂 {os.path.basename(path)}/")

    for idx, entry in enumerate(entries):
        entry_path = os.path.join(path, entry)
        is_last = (idx == total - 1)
        connector = "└── " if is_last else "├── "
        sub_prefix = "    " if is_last else "│   "

        if os.path.isdir(entry_path):
            print(f"{prefix}{connector}📂 {entry}/")
            display_tree(entry_path, ignore_patterns, root_dir, prefix + sub_prefix)
        else:
            print(f"{prefix}{connector}📄 {entry}")


# Run script directly
if __name__ == "__main__":
    root_dir = find_project_root()
    gitignore_path = os.path.join(root_dir, '.gitignore')

    ensure_gitignore_exists(gitignore_path)
    ignore_patterns = parse_gitignore(gitignore_path)
    show_gitignore(gitignore_path)

    print("\n📁 Project Structure (respects .gitignore):\n")
    display_tree(root_dir, ignore_patterns, root_dir)

    # Example usage (for testing)
    # add_gitignore(gitignore_path, 'logs/')
    # remove_gitignore(gitignore_path, 'logs/')
