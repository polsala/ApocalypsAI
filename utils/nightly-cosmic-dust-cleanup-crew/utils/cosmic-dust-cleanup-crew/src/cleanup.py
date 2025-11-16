import os
import sys
import fnmatch
from pathlib import Path

def find_cosmic_dust(path: Path) -> list[Path]:
    """
    Scans the given path for files and directories matching common "cosmic dust" patterns.
    Returns a list of identified dust paths.
    """
    dust_patterns = [
        "*.bak",        # Backup files
        "*~",           # Emacs/Vim backup files
        ".#*",          # Emacs lock files
        "*.tmp",        # Temporary files
        "temp_*",       # Temporary files
        "*.log",        # Log files
        "__pycache__",  # Python bytecode cache directory
        ".pytest_cache",# Pytest cache directory
        ".mypy_cache",  # Mypy cache directory
        ".DS_Store",    # macOS specific metadata file
        "Thumbs.db",    # Windows specific thumbnail cache
        "*.swp",        # Vim swap files
        "*.swo",        # Vim swap files
        "*.orig",       # Merge conflict originals
        "*.rej",        # Patch reject files
        ".vscode/",     # VS Code workspace settings/cache
        ".idea/",       # IntelliJ IDEA workspace settings/cache
        ".env*",        # Environment files (often temporary or local)
        "npm-debug.log",# Node.js debug log
        "yarn-debug.log",# Yarn debug log
        "*.pid",        # Process ID files
        "*.lock",       # Lock files
        "*.sqlite3",    # SQLite databases (often temporary or local dev)
        "*.db",         # Generic database files
    ]

    identified_dust = []

    for root, dirs, files in os.walk(path):
        current_path = Path(root)

        # Check files
        for file_name in files:
            file_path = current_path / file_name
            for pattern in dust_patterns:
                if fnmatch.fnmatch(file_name, pattern):
                    identified_dust.append(file_path)
                    break # Found a match, move to next file

        # Check directories (e.g., __pycache__, .vscode, .idea)
        # We need to check if the directory name itself matches a pattern
        # and if so, add the entire directory and prune it from further walk.
        dirs_to_prune = []
        for dir_name in dirs:
            dir_path = current_path / dir_name
            for pattern in dust_patterns:
                # For directory patterns, we often want to match the full name
                # e.g., "__pycache__" should match exactly, not just "*.cache"
                if fnmatch.fnmatch(dir_name, pattern):
                    identified_dust.append(dir_path)
                    dirs_to_prune.append(dir_name)
                    break
        
        # Prune directories that were identified as dust to avoid scanning their contents
        for d in dirs_to_prune:
            if d in dirs:
                dirs.remove(d)

    return identified_dust

def main():
    target_path_str = sys.argv[1] if len(sys.argv) > 1 else "."
    target_path = Path(target_path_str).resolve()

    if not target_path.exists():
        print(f"Error: Path '{target_path}' does not exist.", file=sys.stderr)
        sys.exit(1)
    if not target_path.is_dir():
        print(f"Error: Path '{target_path}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning {target_path} for cosmic dust...")

    dust_files = find_cosmic_dust(target_path)

    if dust_files:
        print("\nIdentified Cosmic Dust:")
        for dust_path in sorted(dust_files):
            print(f"- {dust_path}")
    else:
        print("\nNo cosmic dust found. Your repository is sparkling clean!")

if __name__ == "__main__":
    main()
