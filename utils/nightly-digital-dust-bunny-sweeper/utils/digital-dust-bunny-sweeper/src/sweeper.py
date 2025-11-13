import os
import fnmatch
import sys

def find_dust_bunnies(root_dir):
    """
    Identifies 'digital dust bunnies' (empty directories and common junk files)
    within the specified root directory.

    Args:
        root_dir (str): The path to the directory to scan.

    Returns:
        tuple: A tuple containing two lists: (empty_dirs, junk_files).
    """
    empty_dirs = []
    potential_junk_items = set() # Use a set to automatically handle duplicates

    # Define patterns for common junk files and directories.
    # These are general patterns and can be extended.
    JUNK_PATTERNS = [
        '.DS_Store',          # macOS directory service file
        'Thumbs.db',          # Windows thumbnail cache
        'desktop.ini',        # Windows custom folder settings
        '*.log',              # Log files
        '*.tmp',              # Temporary files
        '*.bak',              # Backup files
        '*.swp',              # Vim swap files
        '*.pyc',              # Python compiled files
        '__pycache__',        # Python 3 cache directory
        'node_modules',       # Node.js dependencies (often large and temporary)
        'dist',               # Common build output directory
        'build',              # Common build output directory
        '.pytest_cache',      # Pytest cache
        '.mypy_cache',        # Mypy cache
        '.venv',              # Python virtual environment
        'venv',               # Python virtual environment
    ]

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Check for empty directories
        if not dirnames and not filenames and dirpath != root_dir:
            empty_dirs.append(os.path.relpath(dirpath, root_dir))

        # Check for junk files/directories
        for item_name in dirnames + filenames:
            for pattern in JUNK_PATTERNS:
                if fnmatch.fnmatch(item_name, pattern):
                    full_item_path = os.path.join(dirpath, item_name)
                    potential_junk_items.add(os.path.relpath(full_item_path, root_dir))
                    break # Found a match for this item, move to the next item_name

    # Filter out items that are children of other identified junk directories.
    # This ensures we only report the top-level junk directory, not its contents.
    final_junk_items = set()
    # Sort for consistent processing, especially important for path-based filtering
    sorted_potential_junk = sorted(list(potential_junk_items))

    for item in sorted_potential_junk:
        is_child_of_another_junk = False
        for existing_junk in final_junk_items:
            # If 'item' starts with 'existing_junk/' (e.g., 'node_modules/package' starts with 'node_modules/')
            # and 'item' is not the same as 'existing_junk'
            if item.startswith(existing_junk + os.sep):
                is_child_of_another_junk = True
                break
        if not is_child_of_another_junk:
            final_junk_items.add(item)

    # Remove duplicates (handled by set) and sort for consistent output
    empty_dirs = sorted(list(set(empty_dirs)))
    junk_files = sorted(list(final_junk_items))

    return empty_dirs, junk_files

def main():
    path_to_clean = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

    if not os.path.isdir(path_to_clean):
        print(f"Error: '{path_to_clean}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    print("Digital Dust Bunny Sweeper Report:\n")

    empty_dirs, junk_files = find_dust_bunnies(path_to_clean)

    if not empty_dirs and not junk_files:
        print(f"No digital dust bunnies found in '{path_to_clean}'. Your project is sparkling clean! ✨")
        sys.exit(0)

    print("Potential Dust Bunnies Found:\n")

    if empty_dirs:
        print("Empty Directories:")
        for d in empty_dirs:
            print(f"- {d}")
        print()

    if junk_files:
        print("Junk Files/Directories:")
        for f in junk_files:
            print(f"- {f}")
        print()

    print("Consider reviewing and removing these files/directories to keep your project sparkling clean!")
    sys.exit(0)

if __name__ == "__main__":
    main()
