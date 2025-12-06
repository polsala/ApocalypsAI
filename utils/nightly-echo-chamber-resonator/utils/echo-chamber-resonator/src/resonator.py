import os
import sys
import hashlib
from collections import defaultdict

def calculate_file_hash(filepath, hash_algorithm=hashlib.sha256, chunk_size=4096):
    """Calculates the hash of a file."""
    hasher = hash_algorithm()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
    except IOError as e:
        print(f"Error reading file {filepath}: {e}", file=sys.stderr)
        return None

def find_duplicate_files(directory):
    """Finds duplicate files in the given directory based on their SHA256 hash."""
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found.", file=sys.stderr)
        return {}

    print(f"Scanning {directory}...")
    hashes = defaultdict(list)
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_hash = calculate_file_hash(filepath)
            if file_hash:
                hashes[file_hash].append(filepath)
    
    duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    return duplicates

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/resonator.py <directory_path>", file=sys.stderr)
        sys.exit(1)

    target_directory = sys.argv[1]
    duplicate_groups = find_duplicate_files(target_directory)

    if not duplicate_groups:
        print("No duplicate files found. The echo chamber is silent.")
        return

    print(f"\nFound {len(duplicate_groups)} groups of duplicate files:\n")
    group_count = 0
    for file_hash, paths in duplicate_groups.items():
        group_count += 1
        print(f"--- Group {group_count} ---")
        print(f"Hash: {file_hash}")
        for path in paths:
            print(f"  - {path}")
        print()

if __name__ == "__main__":
    main()
