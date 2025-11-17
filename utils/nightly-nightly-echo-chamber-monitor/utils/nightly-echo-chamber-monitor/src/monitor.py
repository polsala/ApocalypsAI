import os
import hashlib
import argparse
from collections import defaultdict

def calculate_file_hash(filepath, hash_algorithm=hashlib.sha256, chunk_size=4096):
    """Calculates the hash of a file."""
    hasher = hash_algorithm()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
    except IOError:
        return None # Handle unreadable files gracefully

def find_duplicate_files(directory):
    """
    Scans a directory for duplicate files based on their content hash.
    Returns a dictionary where keys are hashes and values are lists of file paths.
    Only includes hashes that correspond to more than one file.
    """
    hashes = defaultdict(list)
    print(f"Scanning {directory} for echoes...")

    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.islink(filepath): # Skip symbolic links to avoid issues
                continue
            file_hash = calculate_file_hash(filepath)
            if file_hash:
                hashes[file_hash].append(filepath)
    
    duplicate_sets = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    return duplicate_sets

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Echo Chamber Monitor: Detects duplicate files in a directory."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to scan for duplicate files."
    )
    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Directory not found at '{args.path}'")
        exit(1)

    duplicate_files = find_duplicate_files(args.path)

    if not duplicate_files:
        print("\nScan complete. No echoes detected.")
    else:
        print(f"\nFound {len(duplicate_files)} sets of duplicate files:\n")
        for i, (file_hash, paths) in enumerate(duplicate_files.items()):
            print(f"--- Duplicate Set {i + 1} ---")
            print(f"Hash: {file_hash}")
            for path in paths:
                print(f"  - {path}")
            print()
        print("Scan complete. No more echoes detected.")

if __name__ == "__main__":
    main()
