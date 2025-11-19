import os
import hashlib
import argparse
from collections import defaultdict

def calculate_file_hash(filepath, block_size=65536):
    """Calculates the SHA256 hash of a file's content."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                hasher.update(block)
        return hasher.hexdigest()
    except IOError as e:
        print(f"Error reading file {filepath}: {e}")
        return None

def find_duplicates(directory):
    """Finds duplicate files in the given directory based on content hash."""
    if not os.path.isdir(directory):
        print(f"Error: Directory not found: {directory}")
        return {}

    hashes = defaultdict(list)
    print(f"Scanning {directory} for duplicates...")

    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            if os.path.islink(filepath): # Skip symbolic links to avoid issues
                continue
            file_hash = calculate_file_hash(filepath)
            if file_hash:
                hashes[file_hash].append(filepath)
    
    duplicate_groups = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    return duplicate_groups

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Echo Chamber Purifier: Detects duplicate files by content hash."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The directory to scan for duplicate files."
    )
    args = parser.parse_args()

    duplicate_groups = find_duplicates(args.directory)

    if duplicate_groups:
        print("\nFound {} groups of duplicate files:\n".format(len(duplicate_groups)))
        for i, (file_hash, paths) in enumerate(duplicate_groups.items()):
            print(f"--- Group {i+1} (Hash: {file_hash[:12]}...)")
            for path in paths:
                print(f"  - {path}")
            print()
    else:
        print("\nNo duplicate files found in {}. Your echo chamber is pure!\n".format(args.directory))

    print("Scan complete. Consider reviewing and removing duplicate files.")

if __name__ == "__main__":
    main()
