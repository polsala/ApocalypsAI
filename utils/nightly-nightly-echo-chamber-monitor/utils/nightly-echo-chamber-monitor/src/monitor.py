import os
import hashlib
import argparse
from collections import defaultdict

def calculate_file_hash(filepath, block_size=65536):
    """Calculates the SHA256 hash of a file."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                hasher.update(block)
        return hasher.hexdigest()
    except IOError as e:
        print(f"Error reading file {filepath}: {e}")
        return None

def find_duplicate_files(directory):
    """Finds duplicate files in the given directory based on SHA256 hash.

    Args:
        directory (str): The path to the directory to scan.

    Returns:
        dict: A dictionary where keys are SHA256 hashes and values are lists
              of file paths that share that hash, containing only groups
              with more than one file.
    """
    if not os.path.isdir(directory):
        print(f"Error: Directory not found: {directory}")
        return {}

    hashes = defaultdict(list)
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.islink(filepath): # Skip symlinks to avoid issues like infinite loops or hashing the same content multiple times
                continue
            file_hash = calculate_file_hash(filepath)
            if file_hash:
                hashes[file_hash].append(filepath)
    
    # Filter out unique files (groups with only one file)
    duplicate_groups = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    return duplicate_groups

def main():
    parser = argparse.ArgumentParser(
        description="Detects duplicate files within a specified directory."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The path to the directory to scan for duplicate files."
    )
    args = parser.parse_args()

    print(f"Scanning '{args.directory}' for duplicate files...")
    duplicate_files = find_duplicate_files(args.directory)

    if not duplicate_files:
        print("No duplicate files found. The echo chamber is clear!")
    else:
        print(f"\nFound {len(duplicate_files)} groups of duplicate files:\n")
        group_num = 1
        for file_hash, paths in duplicate_files.items():
            print(f"Group {group_num} (SHA256: {file_hash}):")
            for path in paths:
                print(f"  - {path}")
            print()
            group_num += 1

if __name__ == "__main__":
    main()
