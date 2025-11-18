import os
import hashlib
import sys
from collections import defaultdict

def calculate_file_hash(filepath, hash_algorithm=hashlib.sha256, chunk_size=4096):
    """Calculates the hash of a file's content."""
    hasher = hash_algorithm()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    except IOError:
        return None # Handle unreadable files gracefully

def find_duplicate_files(root_dir):
    """
    Finds duplicate files within a given root directory based on their content hash.

    Args:
        root_dir (str): The path to the directory to scan.

    Returns:
        dict: A dictionary where keys are file hashes and values are lists of file paths
              that share that hash, but only for hashes with more than one file.
    """
    if not os.path.isdir(root_dir):
        print(f"Error: Directory '{root_dir}' not found.", file=sys.stderr)
        return {}

    file_hashes = defaultdict(list)
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            file_hash = calculate_file_hash(filepath)
            if file_hash:
                file_hashes[file_hash].append(filepath)

    duplicates = {
        file_hash: paths
        for file_hash, paths in file_hashes.items()
        if len(paths) > 1
    }
    return duplicates

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/echo_locator.py <directory_path>", file=sys.stderr)
        sys.exit(1)

    root_dir = sys.argv[1]
    duplicates = find_duplicate_files(root_dir)

    if not duplicates:
        print(f"No duplicate files found in '{root_dir}'. Your digital hoard is pristine!")
    else:
        print(f"Duplicate files found in '{root_dir}':")
        for file_hash, paths in duplicates.items():
            print(f"\nHash: {file_hash}")
            for path in paths:
                print(f"  - {path}")

if __name__ == "__main__":
    main()
