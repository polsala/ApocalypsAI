import os
import argparse
from typing import List, Tuple

def find_dust_bunnies(root_path: str) -> Tuple[List[str], List[str]]:
    """
    Scans the given root_path for 'digital dust bunnies':
    - Empty directories
    - __pycache__ directories

    Returns a tuple of two lists: (empty_dirs, pycache_dirs).
    """
    empty_dirs = []
    pycache_dirs = []

    if not os.path.isdir(root_path):
        print(f"Error: Path '{root_path}' is not a valid directory.")
        return [], []

    for dirpath, dirnames, filenames in os.walk(root_path):
        # Check for __pycache__ directories
        if os.path.basename(dirpath) == "__pycache__":
            pycache_dirs.append(dirpath)
            # No need to check if it's also empty, as it's already a pycache
            continue

        # Check for empty directories
        # A directory is empty if it has no subdirectories and no files
        if not dirnames and not filenames:
            empty_dirs.append(dirpath)

    return empty_dirs, pycache_dirs

def main():
    parser = argparse.ArgumentParser(
        description="Scan for 'digital dust bunnies' (empty directories, __pycache__) in a given path."
    )
    parser.add_argument(
        "path",
        type=str,
        help="The root directory to scan."
    )
    args = parser.parse_args()

    print(f"Scanning '{args.path}' for digital dust bunnies...")
    empty_dirs, pycache_dirs = find_dust_bunnies(args.path)

    if not empty_dirs and not pycache_dirs:
        print("No digital dust bunnies found. Your digital space is sparkling clean!")
    else:
        print("\n--- Digital Dust Bunnies Report ---")
        if empty_dirs:
            print("\nEmpty Directories Found:")
            for d in empty_dirs:
                print(f"- {d}")
        if pycache_dirs:
            print("\n__pycache__ Directories Found:")
            for p in pycache_dirs:
                print(f"- {p}")
        print("\n--- End Report ---")

if __name__ == "__main__":
    main()
