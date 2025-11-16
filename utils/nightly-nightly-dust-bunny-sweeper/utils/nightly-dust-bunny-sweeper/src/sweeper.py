import os
import shutil
import argparse
import fnmatch
from typing import List, Tuple, Set

DEFAULT_PATTERNS = [
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".DS_Store",
    "target",  # Rust build directory
    "node_modules",
    "build",   # Common build directory
    "dist",    # Python distribution directory
    "*.pyc",
    "*.log",   # Generic log files
]

def find_dust_bunnies(root_dir: str, patterns: List[str]) -> Tuple[List[str], List[str]]:
    """
    Recursively finds files and directories matching the given patterns.
    Returns two lists: (files_to_delete, dirs_to_delete).
    """
    files_to_delete: Set[str] = set()
    dirs_to_delete: Set[str] = set()

    # Separate patterns into directory names and file patterns (exact or wildcard)
    # Patterns like '__pycache__', 'node_modules', 'target', 'build', 'dist', '.pytest_cache', '.mypy_cache', '.DS_Store'
    # are treated as exact directory names.
    # Patterns like '*.pyc', '*.log' are treated as wildcard file patterns.

    all_dir_names = {p for p in patterns if '*' not in p}
    wildcard_file_patterns = {p for p in patterns if '*' in p}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Check directories
        for dname in list(dirnames): # Iterate over a copy to allow modification
            if dname in all_dir_names:
                full_path = os.path.join(dirpath, dname)
                dirs_to_delete.add(full_path)
                dirnames.remove(dname) # Don't recurse into this directory

        # Check files
        for fname in filenames:
            full_path = os.path.join(dirpath, fname)
            # Check wildcard patterns
            if any(fnmatch.fnmatch(fname, p) for p in wildcard_file_patterns):
                files_to_delete.add(full_path)
            # Check exact file names (if any, though not in DEFAULT_PATTERNS)
            elif fname in all_dir_names: # This means it's an exact file name that matches a dir name pattern
                files_to_delete.add(full_path)
    
    # Filter out files/dirs that are children of a directory already marked for deletion
    final_files = []
    final_dirs = []

    # Sort directories by length in descending order to delete deepest first
    dirs_to_delete_list = sorted(list(dirs_to_delete), key=len, reverse=True)
    
    # Add directories to final_dirs, ensuring no parent is added after a child
    for d in dirs_to_delete_list:
        is_child_of_existing_final_dir = False
        for existing_d in final_dirs:
            if d.startswith(existing_d + os.sep): # Check if d is a child of existing_d
                is_child_of_existing_final_dir = True
                break
        if not is_child_of_existing_final_dir:
            final_dirs.append(d)

    # Add files to final_files, ensuring they are not inside a directory marked for deletion
    for f in sorted(list(files_to_delete)):
        is_in_deleted_dir = False
        for d in final_dirs:
            if f.startswith(d + os.sep): # Check if f is inside d
                is_in_deleted_dir = True
                break
        if not is_in_deleted_dir:
            final_files.append(f)

    return final_files, final_dirs

def sweep_dust_bunnies(files: List[str], dirs: List[str], dry_run: bool = True) -> None:
    """
    Deletes the specified files and directories.
    If dry_run is True, it only prints what would be deleted.
    """
    if dry_run:
        print("\n--- Dry Run: Would delete the following dust bunnies ---")
    else:
        print("\n--- Sweeping dust bunnies ---")

    deleted_count = 0
    for f in files:
        if dry_run:
            print(f"  [FILE] {f}")
        else:
            try:
                os.remove(f)
                print(f"  [DELETED FILE] {f}")
                deleted_count += 1
            except OSError as e:
                print(f"  [ERROR] Could not delete file {f}: {e}")

    for d in dirs:
        if dry_run:
            print(f"  [DIR] {d}")
        else:
            try:
                shutil.rmtree(d)
                print(f"  [DELETED DIR] {d}")
                deleted_count += 1
            except OSError as e:
                print(f"  [ERROR] Could not delete directory {d}: {e}")
    
    if deleted_count == 0 and not dry_run:
        print("No dust bunnies found to sweep!")
    elif deleted_count > 0 and not dry_run:
        print(f"Successfully swept {deleted_count} dust bunnies.")
    elif deleted_count == 0 and dry_run:
        print("No dust bunnies found in dry run.")
    else:
        print(f"Dry run identified {deleted_count} dust bunnies.")


def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Nightly Dust Bunny Sweeper: Cleans up common temporary and build files."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="The root directory to start sweeping from (default: current directory)."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run, showing what would be deleted without actually deleting anything."
    )
    parser.add_argument(
        "--patterns",
        nargs=".", # Use '.' to allow 0 or more arguments, default will be used if not provided
        default=DEFAULT_PATTERNS,
        help=f"Override default patterns. Default: {', '.join(DEFAULT_PATTERNS)}"
    )

    args = parser.parse_args()

    root_path = os.path.abspath(args.path)
    if not os.path.isdir(root_path):
        print(f"Error: Path '{root_path}' is not a valid directory.")
        exit(1)

    print(f"Scanning '{root_path}' for dust bunnies with patterns: {', '.join(args.patterns)}")
    files, dirs = find_dust_bunnies(root_path, args.patterns)

    if not files and not dirs:
        print("No dust bunnies found. Your workspace is sparkling clean!")
        exit(0)

    print(f"Found {len(files)} files and {len(dirs)} directories to sweep.")
    sweep_dust_bunnies(files, dirs, args.dry_run)

    if not args.dry_run and (files or dirs):
        print("\nSweep complete!")
    elif args.dry_run and (files or dirs):
        print("\nDry run complete. To actually sweep, run without --dry-run.")


if __name__ == "__main__":
    main()
