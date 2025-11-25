import os
import hashlib
import sys
from collections import defaultdict

def calculate_file_hash(filepath, hash_algorithm=hashlib.sha256, chunk_size=4096):
    """
    Calculates the hash of a file.
    """
    hasher = hash_algorithm()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
    except IOError:
        return None # File might be inaccessible or not exist

def find_duplicate_files(directory):
    """
    Scans the given directory for duplicate files based on their content hash.
    Returns a dictionary where keys are file hashes and values are lists of file paths.
    Only includes hashes that have more than one file path associated (i.e., duplicates).
    """
    hashes_to_paths = defaultdict(list)
    print(f"🌌 Resonating for echoes in: {directory}\n")

    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            if os.path.islink(filepath): # Skip symbolic links to avoid issues and infinite loops
                continue
            
            try:
                # Skip empty files or files that are too small to be meaningful duplicates
                if os.path.getsize(filepath) == 0:
                    continue
            except OSError: # File might have been deleted between os.walk and getsize
                continue

            file_hash = calculate_file_hash(filepath)
            if file_hash:
                hashes_to_paths[file_hash].append(filepath)
            else:
                print(f"Warning: Could not hash file: {filepath}", file=sys.stderr)

    duplicate_groups = {
        file_hash: paths for file_hash, paths in hashes_to_paths.items()
        if len(paths) > 1
    }
    return duplicate_groups

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/resonator.py <directory_to_scan>")
        sys.exit(1)

    target_directory = sys.argv[1]

    if not os.path.isdir(target_directory):
        print(f"Error: Directory not found: {target_directory}", file=sys.stderr)
        sys.exit(1)

    duplicate_files = find_duplicate_files(target_directory)

    if not duplicate_files:
        print("No echoes found. Your directory is pristine!")
    else:
        print(f"Found {len(duplicate_files)} groups of duplicate files:\n")
        group_count = 0
        for file_hash, paths in duplicate_files.items():
            group_count += 1
            print(f"--- Group {group_count} (SHA256: {file_hash[:12]}...) ---")
            for path in paths:
                print(f"  - {path}")
            print() # Newline for readability

    print(f"Resonation complete. Total {len(duplicate_files)} groups of echoes found.")

if __name__ == "__main__":
    main()
