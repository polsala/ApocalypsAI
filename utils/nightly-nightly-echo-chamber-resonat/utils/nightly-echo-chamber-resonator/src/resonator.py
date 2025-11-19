import os
import hashlib
import argparse
from collections import defaultdict

def _calculate_file_hash(filepath, block_size=65536):
    """Calculates the SHA256 hash of a file's content."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                hasher.update(block)
        return hasher.hexdigest()
    except IOError:
        return None # Handle unreadable files gracefully

def _find_files(directory):
    """Recursively finds all files in a given directory."""
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            if os.path.isfile(filepath):
                yield filepath

def find_duplicate_files(paths):
    """
    Scans given paths (directories or files) for duplicates based on content hash.
    Returns a list of lists, where each inner list contains paths to identical files.
    """
    hash_to_files = defaultdict(list)
    all_files_to_scan = []

    for path in paths:
        if os.path.isdir(path):
            all_files_to_scan.extend(list(_find_files(path)))
        elif os.path.isfile(path):
            all_files_to_scan.append(path)
        else:
            print(f"Warning: Path '{path}' is not a valid file or directory. Skipping.")

    for filepath in all_files_to_scan:
        file_hash = _calculate_file_hash(filepath)
        if file_hash:
            hash_to_files[file_hash].append(filepath)

    return [files_list for files_list in hash_to_files.values() if len(files_list) > 1]

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Echo Chamber Resonator: Find duplicate files by content hash."
    )
    parser.add_argument(
        '--path', 
        nargs='+', 
        required=True, 
        help='One or more paths (directories or files) to scan for duplicates.'
    )

    args = parser.parse_args()

    print("Scanning for echoes...")
    duplicate_groups = find_duplicate_files(args.path)

    if duplicate_groups:
        print(f"\nFound {len(duplicate_groups)} groups of duplicate files:\n")
        for i, group in enumerate(duplicate_groups):
            # Get hash from the first file in the group (all files in group have same hash)
            group_hash = _calculate_file_hash(group[0])
            print(f"Group {i+1} (SHA256: {group_hash}):")
            for filepath in group:
                print(f"  - {filepath}")
            print()
    else:
        print("No duplicate files found. Your file system resonates with unique clarity!")

if __name__ == '__main__':
    main()
