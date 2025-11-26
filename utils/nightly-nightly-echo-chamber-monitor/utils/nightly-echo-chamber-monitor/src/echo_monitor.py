import os
import hashlib
import argparse
from collections import defaultdict

def calculate_file_hash(filepath, block_size=65536):
    """Calculates the SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                sha256.update(block)
        return sha256.hexdigest()
    except IOError as e:
        print(f"Warning: Could not read file {filepath} - {e}")
        return None

def find_duplicates(directory_path):
    """
    Scans a directory for duplicate files based on their SHA256 hash.
    Returns a dictionary where keys are hashes and values are lists of file paths.
    Only includes hashes that have more than one file path associated (i.e., duplicates).
    """
    if not os.path.isdir(directory_path):
        print(f"Error: Directory not found: {directory_path}")
        return {}

    hashes = defaultdict(list)
    for root, _, files in os.walk(directory_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_hash = calculate_file_hash(filepath)
            if file_hash:
                hashes[file_hash].append(filepath)
    
    # Filter out unique files, keeping only duplicates
    duplicate_sets = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    return duplicate_sets

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Echo Chamber Monitor: Detects duplicate files in a directory."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The path to the directory to scan for duplicates."
    )
    args = parser.parse_args()

    print(f"Scanning '{args.directory}' for duplicate files...")
    duplicate_sets = find_duplicates(args.directory)

    if not duplicate_sets:
        print("No duplicate files found. Your file system is pristine!")
    else:
        print(f"\nFound {len(duplicate_sets)} sets of duplicate files:\n")
        for i, (file_hash, paths) in enumerate(duplicate_sets.items()):
            print(f"--- Set {i + 1} (Hash: {file_hash[:8]}...) ---")
            print(f"Original: {paths[0]}")
            if len(paths) > 1:
                print("Duplicates:")
                for duplicate_path in paths[1:]:
                    print(f"  - {duplicate_path}")
            print()

if __name__ == "__main__":
    main()
