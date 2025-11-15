import os
import sys
import fnmatch

def find_dust_bunnies(root_dir):
    """
    Scans the given root directory for 'digital dust bunnies':
    empty directories, files matching common junk patterns, and common junk directories.
    Returns three lists: (empty_dirs, junk_files, junk_dirs).
    """
    if not os.path.isdir(root_dir):
        print(f"Error: Directory '{root_dir}' not found.", file=sys.stderr)
        return [], [], []

    empty_dirs = []
    junk_files = []
    junk_dirs = []

    # Common patterns for junk files
    junk_file_patterns = [
        '*.log', '*.tmp', '*.bak', '*.swp', '*.swo', # Logs, temporary, backup, vim swap files
        '*.pyc', '*.pyo', # Python bytecode files
        '.DS_Store', 'Thumbs.db', # macOS and Windows thumbnail caches
        'npm-debug.log', 'yarn-debug.log', # Node.js/Yarn debug logs
        '.coverage', # coverage.py data
    ]

    # Common patterns for junk directories
    junk_dir_patterns = [
        '__pycache__', # Python bytecode directory
        '.pytest_cache', # pytest cache directory
        '.ipynb_checkpoints', # Jupyter notebooks checkpoints directory
    ]

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Check for empty directories
        # Only add if it's not the root_dir itself and truly empty
        if not dirnames and not filenames and dirpath != root_dir:
            empty_dirs.append(dirpath)

        # Check for junk files
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            for pattern in junk_file_patterns:
                if fnmatch.fnmatch(filename, pattern):
                    junk_files.append(full_path)
                    break # Found a match, move to next file

        # Check for junk directories (among dirnames for the current level)
        for dirname in dirnames:
            for pattern in junk_dir_patterns:
                if fnmatch.fnmatch(dirname, pattern):
                    full_path = os.path.join(dirpath, dirname)
                    junk_dirs.append(full_path)
                    break

    return empty_dirs, junk_files, junk_dirs

def main():
    if len(sys.argv) < 2:
        print("Usage: python dust_bunny_sweeper.py <directory_to_scan>", file=sys.stderr)
        sys.exit(1)

    target_directory = sys.argv[1]
    print(f"Scanning directory: {target_directory}\n")

    empty_dirs, junk_files, junk_dirs = find_dust_bunnies(target_directory)

    all_bunnies = empty_dirs + junk_files + junk_dirs

    if not all_bunnies:
        print("No Digital Dust Bunnies found. Your repository is sparkling clean! ✨")
    else:
        print(f"Found {len(all_bunnies)} Digital Dust Bunnies:\n")

        if empty_dirs:
            print("Empty Directories:")
            for d in empty_dirs:
                print(f"  - {d}")
            print()

        if junk_files:
            print("Junk Files:")
            for f in junk_files:
                print(f"  - {f}")
            print()

        if junk_dirs:
            print("Junk Directories:")
            for d in junk_dirs:
                print(f"  - {d}")
            print()

        print("Sweep complete! Review the list above for potential cleanup.")

if __name__ == "__main__":
    main()
